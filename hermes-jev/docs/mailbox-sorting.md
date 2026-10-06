# Sorting a mailbox, and the four numbers that decide it

`jev mail` answers one question about a pile of mail: **which of these is addressed to me
as a person?** Not how urgent the work is, not who should take it — who wrote it, and
whether it is for me at all. This is what the command decides, what it sends, what it
costs, where it gives up, and when the answer is to use [`jev triage`](../jevkit/triage.py)
instead.

The lane taxonomy and the message-state block are ported from
[fazlerocks/jevmail](https://github.com/fazlerocks/jevmail) (MIT); their notice is in
[NOTICE](../NOTICE). What changed from that original, and why, is in the module docstring
of [`jevkit/mailbox.py`](../jevkit/mailbox.py) and in the changelog. This page is about
running it.

## What it decides

Five lanes — `needs_reply`, `updates`, `promotional`, `sales`, `spam` — and three flags:
`needs_attention` (a person should look), `low_confidence` (the answer was not readable
enough to file on), and `injection` (the body carries text written at whatever agent reads
it). Jev is asked exactly three questions per message: which lane, how urgent on a
five-level rubric, and whether a human wrote this specifically to this recipient.

Jev does not route anything. It returns calibrated readings, and thresholds in our code
turn those into a decision. Every one is a named constant at the top of the module; these
four decide the most:

| Constant | Value | What it holds |
|---|---|---|
| `URGENT_MASS` | 0.40 | Probability mass at "a reply today" + "a person is blocked" before a message interrupts anyone |
| `URGENCY_FLOOR` | 0.30 | The largest single level an urgency answer must hold before it counts as a reading at all |
| `LOW_CONFIDENCE_GAP` | 0.15 | How close the runner-up lane may be before the message is marked unsure |
| `CALIBRATED_ENOUGH` | 0.50 | Jev's own confidence, below which nothing is dropped into a disposal lane unseen |

`URGENCY_FLOOR` is the one worth understanding, because it is why this module exists. On a
live bank alert Jev answered with a *flat* urgency distribution — 0.2 on each of five
levels, confidence 0.0 — and a point estimate of 2.73. Rounding that point estimate stores
"4 of 5", a level nobody chose, from an answer that said nothing. Five levels flat also
puts exactly 0.40 at the top two, which is `URGENT_MASS` to the digit. So a spread with no
peak anywhere is not a quiet message and not an urgent one: it is no reading, it is
reported as `urgency spread too flat to read`, and it sets `needs_attention`.

The same instinct runs through the rest. A human plainly writing to this person is lifted
out of `promotional` and `spam` whatever the lane said. Urgency speaks in `updates` as well
as `needs_reply`, because every example this was built from — a card decline, an OTP, a
fraud notice — is `updates` by the taxonomy's own definition. And an uncalibrated answer
never files mail into a disposal lane. Unsure mail stays where a person will see it.

## What leaves the machine

Per message: subject and up to 2,500 characters of body, both redacted; the sender's
domain, never the mailbox; a locally derived sender class; the timestamp; two header facts;
and nothing else. The address itself is never sent in any encoding it could have arrived in
— see the `readable` docstring for the three ways one newsletter footer got a recipient's
own address onto the wire at once.

The sender class deserves a note, because it was wrong until recently. It has four values:

- `automated` — the address cannot receive a reply: `noreply@`, `no-reply@`,
  `mailer-daemon@`, `bounces@`, an autoresponder. Read off the parsed address, because
  `From:` in real mail is `Acme Billing <noreply@acme.test>` and splitting that on `@`
  gives `acme billing <noreply`, in which none of those names starts a label.
- `list` — a `List-Unsubscribe` header, or a bulk-shaped name (`newsletter@`, `digest@`).
- `role` — a shared mailbox a team reads: `support@`, `billing@`, `orders@`, `postmaster@`.
- `person` — everything else.

`role` used to be folded into `automated`, so a colleague writing from their team's shared
address, or a customer replying from `billing@`, was reported to Jev as a machine. "A
machine wrote this" pushes a message away from `needs_reply`, which is the single failure
this module exists to prevent — and RFC 2142 requires that a *person* read `postmaster@`
and `abuse@` at all. The robot signal is real and worth sending; it is only worth sending
about robots.

## The injection screen

A mail body is the most attacker-controllable text an agent will ever read. Anyone who
learns the address can put words in it, and `jev mail` hands its rows straight into an
agent's context. So the same screen this repo runs on retrieved memory passages —
`rerank.local_screen` — runs on every decoded mail body here, with `unvetted=True`, because
none of the three questions asked of Jev is "is this aimed at the agent".

What it catches is **flagged, never filed away and never deleted**. The row keeps its lane,
gains `injection: "<shape>"`, and says so in `reason`. The reason for that asymmetry is
worth stating plainly: if a screened message disappeared, then a sentence in a body would
be the most useful thing an attacker could reach in this whole command. Flagging costs a
person one glance; deleting costs them the message.

The message is still sent to Jev. One message is one request, so text written to steer a
model can only reach the answer about itself — unlike a rerank batch, where one poisoned
passage rides along with forty others — and Jev answers with probabilities, not prose.

### One shape does not call a person over

`rerank.local_screen` was tuned against 11,299 passages cut from open-source READMEs. Mail
is a different distribution, and nobody had measured it, so 30 hand-written non-attack
bodies across the five lanes were run through it. Two flagged, and both were the `command`
shape: a code-host notification quoting a comment that said `rm -rf node_modules`, and a
release note whose install line is `curl … | sh`. Neither is addressed to an agent. Both
are addressed to the reader's shell, which is how release notes have always talked.

So `command` is recorded on the row and listed in the summary, and it does not set
`needs_attention` by itself. Every other shape does — `instruction`, `image-beacon`,
`url-fill-in`, `url-substitute`, `link-flood` — because the rest only make sense if
whoever wrote the mail expected a model to read it. The rule is written as membership of
that one shape rather than as a list of the others, so a shape added to `rerank` later
escalates until somebody measures it against mail the way these were. `needs_attention`
is the one flag this command exists to make mean something; a screen that marks a quarter
of a mailbox is a screen nobody reads.

Measured cost of the screen: about 0.1 s on a 62,000-character HTML newsletter, inside the
same worker pool as a Jev call that took about 0.5 s in the same run. The worst case
measured is about 0.36 s, on 64,000 characters that are almost all URLs — the screen is
pure CPU and the Jev call is not, so a batch of link-dense newsletters is the case where
the pool stops being eight-wide.

## What it costs, and how that number is derived

The old summary multiplied the row count by a flat 450 tokens a message. Against the live
endpoint a full-length message counts 1,402. The old figure was a third of a real batch,
and no test could catch it, because the check repeated the same arithmetic.

Now nothing is assumed. `summarize()["cost"]` prices only messages Jev answered, and for
each one it uses, in order:

1. the input-token count the provider put in its own reply — which today's endpoint sends
   for every request, so this is the path a real batch takes; or
2. the characters this module measured itself putting in that request, converted by
   `tokens_from_chars`.

A count that is not a finite number — `Infinity` and `NaN` are both valid to
`json.loads`, and so is any literal past the float ceiling — is treated as no count at
all rather than converted, because `int(float("inf"))` is an `OverflowError` and
`classify` promises it never raises.

The total is multiplied by `INPUT_USD_PER_MTOK` (0.042, the published input price — the
only number in the figure that is neither counted nor read back). `from_provider_counts`
and `from_measured_characters` say how many rows took each path, and `unpriced_messages`
says how many the figure does not cover at all. With nothing to count, `usd` is `null`
rather than `0.0`, because a batch nobody could price is not a batch that was free.

Four live requests, with the provider's own count beside each:

| Message | Request body | Input tokens | USD |
|---|---|---|---|
| Short personal note | 1,906 chars | 748 | $0.00003 |
| Newsletter with an unsubscribe header | 1,919 chars | 747 | $0.00003 |
| Medium reply | 2,715 chars | 914 | $0.00004 |
| Full length (300-char subject, 2,500-char body) | 4,678 chars | 1,402 | $0.00006 |

Those four are also what the character fallback is fitted to, which is why it is affine
rather than a single ratio: every request carries the same three questions and the same
JSON scaffolding, and that fixed part tokenizes much denser than prose. The best single
chars-per-token ratio through these points is 21% low on a short message and 4% high on a
long one; `REQUEST_FIXED_TOKENS + chars / CHARS_PER_TOKEN` is within 3% of all four, and a
test holds it there.

All four of those requests are Latin script, and that is a limit of the fallback, not of
the counts. The request body is JSON with the default escaping, so a CJK or Cyrillic body
goes on the wire at six characters per character: a 2,400-character Japanese message
measures 16,280 request characters where an English one of the same length measures about
2,700. Nothing here has measured what the provider counts for that, and no ratio was
invented for a script nobody measured — which is the whole reason the provider's own count
is the path that runs and `from_measured_characters` tells you when it did not.

Output is not priced: Jev returns a typed answer, not prose. If a provider bills output
separately, treat the figure as a floor.

## Fail open, always

Every failure path ends the same way: a row, a `reason`, and `needs_attention: true`. Jev
unavailable, no key, a transport that dies mid-read, an answer outside the lane set, a
message with nothing to read, a message that looks like it holds a credential. The command
still exits 0 and still returns one row per message it was handed, carrying the same set of
fields on every path, because a consumer reading `row["urgent_mass"]` should not get a
`KeyError` on exactly the rows that need a person.

Two habits make that promise real in a pipeline:

- Treat a verdict as an *opinion about* the mail, never a *dependency of* handling it. The
  four rules in [wiring triage into a live pipeline](wiring-triage-into-a-live-pipeline.md)
  apply here without change — especially shadow mode before anything is allowed to steer.
- Never let a lane move mail while `needs_attention` or `low_confidence` is true. Those two
  flags are the whole safety margin.

## Choosing between this and `jev triage`

They overlap, and the difference is the question, not the quality.

| | `jev mail` | `jev triage` |
|---|---|---|
| Asks | Is this addressed to me as a person? | How soon does this need a response, and from whom? |
| Input | A mailbox export, in batches | One message, as it lands |
| Output | 5 lanes, plus attention / unsure / injection flags | 4 routes (`now`, `today`, `queue`, `ignore`), plus kind, blocked, deadline, actionable, frustrated |
| Signals it has | `List-Unsubscribe`, whether you replied in the thread, sender domain and role | Your customer domains, so a known customer reporting a problem is never ignored |
| Fails open to | `needs_attention: true`, no lane | `route: "today"` |
| Request size | 4,678 chars on a full-length message | 4,635 chars on the same one |

Cost is not the deciding factor — the two requests are within a percent of each other in
size. Pick by the question:

- **A personal inbox, a backlog, an unread pile, "what did I miss while I was away"** →
  `jev mail`. It knows about mailing lists, and it is the only one of the two that will
  tell you a message came from one.
- **A shared support address, a ticket feed, anything with an SLA** → `jev triage`. It is
  built to run on every message as it arrives, it knows which domains are customers, and
  its output is a work queue rather than a set of trays.
- **Both** is defensible on a mixed mailbox where personal mail and customer mail land
  together: sort first, then triage what landed in `needs_reply`. It costs two requests per
  message, so do it on the lane, not on the mailbox.

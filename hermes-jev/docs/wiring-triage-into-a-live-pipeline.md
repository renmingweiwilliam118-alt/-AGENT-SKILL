# Wiring triage into a pipeline that already works

`jev triage` on its own is a command you run when you remember to. The value only
arrives when every message is classified as it lands — which means editing something
that is already carrying real traffic. This is how that was done on a live support
inbox, and the four rules that made it safe to do at all.

The reference adapter is [`scripts/triage_adapter.py`](../scripts/triage_adapter.py).
Copy it, change the three constants at the top, and read the rules below before you
wire it to anything.

## 1. Fail open, or don't ship it

The pipeline collected mail before triage existed. It must collect mail if triage
breaks. No key, no network, a timeout, a malformed answer, the toolkit not installed at
all — every one of those has to end with the message routed exactly as it would have
been, and the cycle exiting zero.

That means every entry point returns `None` instead of raising, and the caller reads
`None` as "no opinion":

```python
verdict = None
if engine is not None and budget > 0:
    budget -= 1
    verdict = classify_brief(brief, tenant=tid, domains=domains, module=engine)
    if verdict is not None:
        record(TRIAGE_FILE, verdict, mode=mode)
```

Three of the tests that ship with this pattern exist only to hold that line: the
classifier raising, the toolkit missing, and the module absent entirely. All three must
end with `new_records == 1`.

This is not defensive-programming garnish. A classifier is an *opinion about* the work,
never a *dependency of* the work. The moment an opinion can stop mail being collected,
you have made the system worse than the regex it replaced.

## 2. Shadow before it steers

Give the integration three modes and default to the middle one:

| mode | classifies | records | changes routing |
|---|---|---|---|
| `off` | no | no | no |
| `shadow` | yes | yes | **no** |
| `on` | yes | yes | yes |

In `shadow` you get the full cost and the full latency and a complete log of what the
classifier *would* have done, while the pipeline behaves exactly as it did yesterday.
Then a person reads a batch of verdicts and decides whether it has earned the switch.

This is the same discipline the model router uses, and for the same reason: the first
policy that felt right escalated 89% of turns, and shadow mode is the only thing that
caught it before it cost anything. A classifier that starts steering traffic before
anyone has read its output is how you end up paging someone about a newsletter — and
crying wolf once trains everyone to ignore the pile forever.

## 3. Respect the emit contract you found

The router this was wired into carried a promise in its own docstring: *"never bodies,
never subjects, never addresses beyond domain."*

Triage needs the body to be any good. That is not a conflict — a body **read** to
classify is not a body **persisted** — but it is only not a conflict if you are
deliberate about it. Read the body, classify, drop it. What lands on disk is an id, a
domain, a route and some numbers:

```json
{"id": "287d5b89", "message_id": "imap-uid:15:5c71...", "domain": "example.com",
 "tenant": "acme", "route": "queue", "urgency": 1.18, "kind": "request",
 "confidence": 0.85, "blocked": 0.13, "sent_to_jev": true, "latency_ms": 491}
```

A stored route with no subject is unreadable to a human, so the adapter ships a
`review` that re-joins ids against the messages *where they already live* and renders
subjects on demand. The readable view is built when asked for; nothing is copied.

Pin it with a test that puts a distinctive string in the subject and body and asserts
neither appears in the written file. That test is the contract.

## 4. Bound the work, and prove it where it actually runs

A cycle on a timer must not be able to turn a backlog into a long-running job. One
constant — `MAX_PER_CYCLE` — and a test that feeds it more messages than the budget and
asserts every message is still *routed* while only `MAX_PER_CYCLE` are *classified*.

Then prove it in the real harness, not in a shell. A unit test and a hand-run command
both pass in your interactive session, which has your environment, your PATH and an
unlocked keychain. The scheduler has none of those guaranteed.

The honest test is: take one benign, already-processed message, mark it unprocessed,
let the **scheduler** run its own cycle, and read the record it wrote.

```
{"route": "queue", "sent_to_jev": true, "latency_ms": 491, ...}
```

`sent_to_jev: true` from a job the scheduler started is the only proof that the secret
store is reachable from where the code actually lives. Everything before that was proof
about your shell.

## Reading the pile

```bash
python3 scripts/triage_adapter.py --route now --route today
```

```
now=3  today=2

now    u=3.91  problem    example.com    Checkout is down for everyone
now    u=2.79  problem    example.com    Cannot open any of today's orders
today  u=2.68  request    example.com    Add a user to the shared workspace
```

## What the numbers looked like

75 real support messages, classified in one pass:

| route | count |
|---|---|
| now | 23 |
| today | 6 |
| queue | 45 |
| ignore | 1 |

$0.0047 for all 75, p50 latency 501ms. Three messages never reached Jev at all — the
privacy gate caught credentials in them and escalated them to a person, which is the
right answer on both counts.

A 31% `now` rate is high, and worth saying plainly rather than hiding: that corpus is
months of a rocky rollout plus deliberate test messages, not a steady-state inbox. The
rate is a fact about those months. Shadow mode exists precisely so that judgement is
made on real numbers by a person, and not by whoever wrote the thresholds.

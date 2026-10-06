# Response caches, and what we built instead

We were asked whether [Computer-Use Cache](https://github.com/rohanarun/computer-use-cache)
(MIT) belongs in this repo. It does not, and the reasons are worth keeping, because the same
question will come back about the next cache proxy.

## What it is

An OpenAI-compatible proxy. It hashes a chat-completions request, and when the same request
arrives again it returns the stored response without calling the provider. Exact match only.
An optional mode asks Jev whether a stored response for a *similar* request can be reused; we
have not evaluated that judge, so nothing here is a claim about it either way.

## Why it does little for a Jev-driven loop

A response cache saves a model call. In our loops that call is already the cheap part.

- A Jev decision takes about 0.47 s and costs about $0.00006. One hop of the desktop loop is
  about 4.2 s, and about 2.6 s of that is the driver confirming that the click landed.
- In one measured agent run the runner took 7.9 s of a 36.4 s wall clock. The rest was the
  agent's own turns around it. No cache reaches those: they are streamed, they carry a
  transcript that grows every turn, and so no two are ever byte-identical.

## Why it does nothing for a Hermes lane today

- Hermes streams its main loop, and the proxy never stores a streamed miss. It forwards the
  stream and writes nothing, so there is never an entry to hit.
- A Hermes plugin can swap the *model* for a turn. It cannot swap the *provider connection*,
  and a proxy is a provider connection. Putting one in front of a lane is a change to that
  lane's provider configuration, not something a skill or plugin from this repo can do.

## If you run the proxy anyway

Its defaults are for a demo: all interfaces, any origin, open admin endpoints.

- Leave `UPSTREAM_API_KEY` unset on the proxy, so each client's own bearer token is forwarded.
  Set, it becomes a key that anything able to reach the port can spend.
- Set `CORS_ALLOW_ORIGIN` to one origin (the default is `*`), set `CACHE_ADMIN_TOKEN` (without
  it the stats and clear endpoints are open), and bind it to `127.0.0.1`.
- Pin a commit. It sits on the path of every request and every bearer token.
- Never put it behind `TEXT_MODEL_BASE_URL` for a logged-in site. Requests to that endpoint
  carry text taken from the page, and the proxy writes request bodies to disk in plain text.
  Its secret screen only recognises `name = value` assignments, so a bare token, a cookie or
  a customer's message goes straight into the database.
- Pointing `TEXT_MODEL_BASE_URL` at a local proxy silently drops our reasoning-off flag:
  `jevkit/plan.py` sends it only when the host is `openrouter.ai`. Plans get slower, and a
  reasoning model can spend the token ceiling before any JSON appears.

## What we built instead: the plan cache

The one call in this repo whose answer is a function of its input is `jev plan` / `--plan`:
one text-model call, about 1 s and about $0.0006, repeated for every repeated spoken command.
`jevkit/memo.py` is a small exact-match store and `jevkit/plan.py` uses it. Two ideas are
borrowed from Computer-Use Cache and credited in the code: the key names the endpoint the
answer came from, and any failure is a miss. No code is.

### What it hit, before we measured it

0.14.0 shipped the cache in shadow and nobody checked whether it was worth having. It keyed
on the command byte for byte. These commands are **dictated**, so we drove `plan()` with an
injected transport over 19 repeats of six spoken commands — the same sentence transcribed
the ways a dictation engine really varies it: a capital on the first word, a capital on an
app name, the full stop it adds at the end, a doubled space.

**It hit once. 5%.** Eighteen of nineteen repeats of something the person had already said
were a second model call for a plan already sitting on disk, and the one hit was leading and
trailing whitespace, which `strip()` had handled since the first version. A cache that only
hits on byte-identical input, in a system whose input is speech, is worth very close to
nothing, and that is what it was.

The corpus is not a note of what we saw once: it is `PlanCacheTests.DICTATED` in
`tests/test_plan.py`, and both figures in this page are asserted by tests next to it, so you
can re-measure rather than take our word for it.

### What is keyed now

Two keys, one file. Both carry the front app (because "open a new window" means a different
menu in a different app), the running apps *the command names* (the full list is z-ordered
and changes every run, so it is left out; the model still gets it on a miss), the model, the
endpoint's hostname, and a hash of the prompt, the step schema, the vocabulary, the step
limit and the never-send rule version. Edit the prompt and every old entry stops matching.
There is no fingerprint of the API key.

They differ in how they carry the command:

- the **exact** key holds it byte for byte, spacing included;
- the **loose** key holds one utterance rather than one transcription of it: case-folded,
  inner whitespace collapsed, trailing engine punctuation removed.

A plan is written to the loose key **only when no field of it is a copy of the command's
exact characters**. Exactly two fields can be: the text of a `type_text`, which is typed
character for character, and the path of an address, because `/Docs` and `/docs` are
different pages. Everything else a step can hold — an app name, an on-screen target, a menu
path, a key name, a count — is matched case-insensitively by whatever receives it. A plan
that types dictated words, or opens an address with a path, stays on the exact key, where
"write: Buy milk" and "write: buy milk" remain the two different commands they are. A read
from the loose key checks the same thing again before serving, because the file is not ours.

"The apps the command names" is decided by looking each running app's name up in the
command, and that lookup collapses whitespace on both sides. It did not, at first, and the
doubled space this page keeps talking about was enough to defeat it: `Switch to Visual
Studio Code` said with a doubled space inside the name does not *contain* "visual studio
code", so the app went unnamed — and an app that goes unnamed is an app whose being open or
not has dropped out of the key. Measured: that command gave the same key with the app
running and with it closed, and the plan kept for the machine where it was open (click it in
the dock) was served to the machine where it was not running at all. Word-level rewrites we
do not attempt are one thing; losing a correctness field to the exact variance the loose key
was built for is another.

**Measured on the same 19 repeats: 5% → 68%.** The six that still miss are the honest ones:
every one of them dictates a note or a search term, so its plan types the command's exact
characters and cannot be shared without typing words this transcription does not contain.
Pairs that a human would call *different* commands — a different sentence, a different front
app, the named app running or not (with either spacing), different dictated text, different
spacing inside dictated text, `/Docs` against `/docs` — all still miss, as they must.

Two kinds of near-miss are left on purpose, because neither follows from "the plan would
have been the same": an inserted comma (`Open Safari, and go to example.com`) and a
politeness wrapper (`Please open Safari`). Stripping punctuation anywhere but the end of the
sentence would merge `ex.ample.com` with `example.com`, and dropping words is a rewrite
whose failure mode is the never-send filter losing the word the person actually said.

So: worth having now, and it was not before. If your commands mostly carry dictated text,
expect something much nearer the 5%.

**What is never stored.** A command `privacy.is_sensitive` flags returns before a key is even
computed. A plan with a step whose target or text looks sensitive is returned and not kept. A
fallback is never kept. Entries hold validated steps only: no prompt, no reply, no key. They
live in `$XDG_CACHE_HOME/jev/memo/plan.json` (default `~/.cache`), mode 0600 in a 0700
directory, at most 256 entries, for 7 days. Deleting the file is always safe.

**7 days now means removed, not just ignored.** It used to mean only ignored. Expiry was a
refusal to *serve*, and an entry left the file solely as a side effect of storing a new one
in the same run — so we measured which runs store nothing. Of six kinds of run, five
left a ten-day-old dictated note sitting there: a cache hit, an outage, a shadow run whose
stored plan agreed, a plan whose steps looked sensitive, and `JEV_MEMO=off`. Every `plan()`
that is not `off` now clears the expired entries out first, and rewrites the file only when
something really expired. `off` still does not, because `off` reads nothing and writes
nothing — that is the contract, and it is why `jev memo clear` exists.

What *is* stored, in `shadow` as well as `on`, includes the words a command dictates: the text
of a `type_text` step, in plain text. "Looks sensitive" means looks like a secret, not looks
private. If dictated text must not sit on disk for a week, set `JEV_MEMO=off` **and run
`jev memo clear` once**: `off` stops the next plan being written, and stops nothing being
read, written or tidied, so it never removes what is already there.

**What is still checked.** The cache is a file, so it is not trusted. On every read each step
goes back through the same validation as a model's reply, then through the never-send filter
under today's rules; a hand-edited Send step is dropped like any other. And a cached plan only
replaces the *planning* call. Every step is still observed, chosen, executed and verified
exactly as before. A run that fails a step or ends unverified forgets its plan.

**Modes.** `JEV_MEMO=off|shadow|on`, and `shadow` is the default (see
[turning a Jev feature on](turning-a-jev-feature-on.md)). In `shadow` the model is always
called and nothing is reused; the result's `cache` field records `miss` (no entry yet),
`shadow_agree` (the stored plan equals the fresh one) or `shadow_differ` (it does not, and is
overwritten). `on` reports `hit` or `miss`; `off` reads and writes nothing.

`jev memo stats` shows how many plans are stored and how large the file is: a namespace, a
count, a size. Never a key, and never any part of a plan — it is the one thing people paste
into an issue, and there is a test that stores a plan with a distinctive phrase in it and
reads the command's whole output back. `jev memo clear` empties it.

**Two processes at once.** Both read the file, both add an entry, both write; `os.replace`
makes the swap atomic, so the second one wins whole and the first one's entry is gone. That
is the only thing that happens, and we ran four processes writing the same namespace flat
out to check: never a half-written file, never a merged one, never a torn value, never a
temp file left behind, and every entry still in it was one some process really wrote.

The loss is not small when they genuinely collide — about a third survives: 120 writes from
four processes left 33 to 35 entries over repeated runs, and 246 writes from six left 43.
It costs exactly one model call per lost entry, the call that would have been made without a
cache at all, and one person dictating one command at a time never sees it. A lock would
instead cost every caller a way to hang. Since every `plan()` that is not `off` now purges on
its way past, a *reader* can drop a writer's entry too; that is the same one-call loss, and
the read itself is unaffected — `os.replace` means it either sees the old file whole or the
new one whole.

**Before turning it on,** read a batch of `cache` values from your own `--json` results
(`plan.cache`). Mostly `miss` means commands do not repeat and the cache buys nothing. A
`shadow_differ` means the model gave two different plans for the same command in the same
context: read both, because with `on` you would have got the older one. Turn it on when the
repeats agree. A cache can only ever be as right as the first answer it kept.

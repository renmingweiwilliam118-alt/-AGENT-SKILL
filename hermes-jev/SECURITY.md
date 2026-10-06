# Reporting a security or privacy problem

Please do not open a public issue. Use GitHub's private reporting on this repo
(**Security → Report a vulnerability**), which reaches the maintainer and nobody else.

Say what you found, the smallest way to see it again, and what it would let someone do.
You do not need a proof-of-concept exploit. Expect a first reply within a few days; if the
report is right, you will be named in the fix unless you would rather not be.

## What counts here

This project hands decisions to a cloud API and drives a keyboard, so the interesting
problems are mostly about what leaves a machine and what an agent can be talked into:

- **Something leaves the machine that shouldn't.** The README's "What leaves your machine"
  section is a promise. A case where more than that is sent — through an encoding, a
  truncation, a log, a cache file, an error message — is a bug of this kind, and it is the
  most valuable thing you can find. Two have been fixed this way already.
- **A key becomes reachable.** In a log, an error, a crash, a cache, a `.env` written too
  widely, or a page served by `jev setup-key`.
- **Prompt injection that survives a screen.** Text in a retrieved passage, a mail body or
  a page that gets an agent to act on it. `jevkit/rerank.py` screens for this; a bypass is
  worth reporting.
- **An action escaping its gate.** The computer-use and browser runners may only execute an
  action the application itself put in the table, and never a send, pay or delete that the
  person did not ask for (`jevkit/plan.py`, `enforce_never_send`). A way around that is
  serious.
- **A cached plan or capsule serving something it shouldn't**, or surviving a run that
  ended unverified.

## What doesn't

- A missing key, a rate limit, or Jev being down. All of those are expected; everything
  fails open by design, and a case where something *doesn't* fail open is an ordinary bug.
- Anything needing an attacker who already runs code as you on your own machine.
- The Jev model's answers themselves. Those belong with [TypeSafe](https://docs.typesafe.ai).

## When you report

Redact before you paste. A transcript, a mail body or a decision log from a working
machine is exactly the kind of thing this project exists to keep private, and a report is
not an exception. Invented data that shows the same shape is always enough.

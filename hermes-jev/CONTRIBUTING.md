# Contributing

Contributions are welcome, and small ones are the most welcome of all. If you have found
a decision an agent is paying a frontier model to make, that is the thing this repo wants.

**If you are here for the first time:** open a PR. You do not need to ask first, you do not
need to match the house style perfectly, and you do not need to have solved the whole
problem. Something that works with a test beside it is enough to start from.

## Before you spend an evening on it

Two things have bitten every contributor to this repo, including its author, so they are
worth knowing before rather than after:

**A green run on your machine is not a green run.** CI is Ubuntu and macOS on Python 3.9
and 3.13. Two kinds of test pass locally and fail there: tests that quietly read your own
keychain, and tests that patch a function which was bound as a default argument
(`def f(..., opener=subprocess.run)` binds at import, so patching the module afterwards
does nothing — that one had the suite launching real apps on the author's Mac for a week).
Both have happened; both now have tests that catch them. If you have Docker or Apple's
`container`, one command saves the round trip:

```bash
container run --rm -v "$PWD":/w -w /w python:3.13-slim python -m unittest discover -s tests
```

**Jev's confidence is calibrated, and everything here reads it as such.** The 0.65 floor
before a GUI action, the 0.7 floor before a transcript turn is dropped, "unsure is not
hard" in the router — all of them assume a real probability. Substituting a language model
that reports its own confidence silently changes every one of those thresholds without
failing anywhere visible. If a feature needs a model that is not Jev, it belongs behind a
different name and its own threshold.

## The sync rule

This repo is the public home of everything Jev does for a Hermes agent. If Jev's role changes in a working Hermes setup, this repo changes in the same piece of work:

- a new decision handed to Jev, or one taken away
- a changed question, threshold, time budget or fail-open behaviour
- a change to what is sent to Jev (the privacy boundary)
- a fix to the plugin, the key flow or the installer
- a new Hermes seam the plugin uses, or one that went away
- any change to the model routing dashboard (`router-dashboard/` is its only source; the running service is started from this checkout)

Each change comes with a test in `tests/`, an updated `SKILL.md` if an agent would do something differently, and a line in `CHANGELOG.md`. Bump `jevkit/__init__.py` and `hermes/plugin/hermes-jev/plugin.yaml` together.

## What never goes in

Keys, tokens, `.env` files, routing pools or decision logs from a real machine, customer or personal data, and machine-specific absolute paths. Run the check before you push:

```bash
python3 -m unittest discover -s tests && python3 scripts/check_release.py
```

## Ground rules for the code

- Standard library only. The point is that any agent can run it with whatever `python3` is on the machine.
- Every call to Jev goes through `jevkit/client.py`, and everything sent goes through `jevkit/privacy.py` first.
- Every feature has a fail-open path that is exactly what the agent would have done without Jev, and a test that proves it.
- Jev picks from closed sets that code built. It never produces text, coordinates, commands or arguments that get executed.
- Tests are offline: fake the transport, never call the real API, never touch a real secret store.

## Review, and what happens to your PR

Every PR gets a run of the suite on four platform/version combinations, and a read by a
person. What a review looks for, in this order:

1. **What leaves the machine.** The README's "What leaves your machine" section is a
   promise to everyone running this. Any change to it is the first thing discussed.
2. **The fail-open path.** No key, no network, a slow answer, a malformed one: the agent
   carries on exactly as it would have without Jev.
3. **A test that would have caught the bug.** Not coverage for its own sake — the specific
   case that was wrong.
4. Style, naming and comments. Last, and never a reason to reject anything.

If a change is right in idea but not in mechanism, expect that said plainly, with the
reasoning, and the idea credited to you either way. That has already happened once: the
OpenRouter support in 0.16.0 is someone else's idea, implemented differently, and the
reasoning is in the CHANGELOG and on the PR.

Credit is not a formality here. Contributors are named in `CHANGELOG.md` for the release
their work lands in, kept as the commit author or a `Co-Authored-By:` trailer so GitHub
attributes it, and named in `NOTICE` if their project is ported from.

## Security and privacy

Do not open a public issue for those. [SECURITY.md](SECURITY.md) says how to report one
privately, and what kinds of finding matter most here.

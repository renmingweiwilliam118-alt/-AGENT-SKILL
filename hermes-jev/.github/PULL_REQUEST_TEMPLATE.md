<!-- Thank you. A short PR with a test beats a long one without. -->

## What this changes

<!-- One or two sentences. If it fixes something, say what went wrong, not just what you changed. -->

## Why

<!-- What did you hit that made this necessary? A real story is more persuasive than a rationale. -->

## How it was checked

<!-- Delete what does not apply. -->

- [ ] `python3 -m unittest discover -s tests` passes
- [ ] `python3 scripts/check_release.py` is clean
- [ ] A test that fails before this change and passes after — say its name:
- [ ] Ran it against real Jev, or explained why that was not possible

## The two things reviewers will look at first

- [ ] **Nothing new leaves the machine.** If this changes what is sent to Jev or any other
      service, say exactly what, and check it against the "What leaves your machine"
      section of the README.
- [ ] **It fails open.** If Jev, a key, the network or a file is missing, the agent carries
      on as it did before. Nothing here raises into a caller that did not raise before.

<!--
Two things worth knowing, because they have both bitten this repo:

1. A green run on your machine is not a green run. CI is ubuntu + macOS on 3.9 and 3.13.
   Tests that read your keychain, or that patch a function bound as a default argument,
   pass locally and fail there.
2. Jev answers with a CALIBRATED confidence, and every threshold here reads it as one.
   Anything that substitutes a language model's self-reported confidence quietly changes
   all of them. If you need a model that is not Jev, it belongs behind a different name.
-->

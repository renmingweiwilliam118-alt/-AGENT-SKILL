# Compaction scorecard, 2026-09-20

Seven real working sessions (243 to 614 rows, 12 to 194 user/assistant turns, 25,000 to
118,000 characters of dialogue, all with heavy tool use). A 15-question recall exam each;
104 of the 105 questions were answerable by an oracle with the whole transcript, and
recall is scored on those. Writer and answers `z-ai/glm-5.3-flash`, exam and judge
`google/gemini-3.8-flash`, Jev `jev-latest`. Method and caveats in [../README.md](../README.md).

Nothing below is session content. Transcripts, exams and capsules stay off this repo.

## What was shipping, against the free alternatives

Same 400-word capsule, same writer. "Writer reads" is the average prompt size.

| arm | closed-book | with one search | writer reads | Jev |
|---|---|---|---|---|
| `plugin_fallback`: plain last 24,000 chars | **48.1%** (50) | 68.3% (71) | 24,940 | none |
| `full`: the whole dialogue | 46.2% (48) | 67.3% (70) | 88,609 | none |
| `tail_plain`: last 24,000 chars, plain prompt | 40.4% (42) | **73.1%** (76) | 24,770 | none |
| **`jev`: what shipped through 0.13.2** | 37.5% (39) | 68.3% (71) | 17,434 | 13 calls, 7.8 s |
| `failopen`: what a Jev outage gave | 33.7% (35) | 61.5% (64) | 12,511 | none |
| `regex_keep`: keep identifier-shaped turns | 31.7% (33) | 62.5% (65) | 24,940 | none |
| `recency_matched`: Jev's counts, by recency | 30.8% (32) | 60.6% (63) | 12,757 | none |
| `none`: no capsule at all | n/a | 56.7% (59) | 0 | none |

Question by question, on the 104:

| comparison | closed-book | with one search |
|---|---|---|
| `jev` against the plain tail | 4 won, 15 lost | 11 won, 11 lost |
| `jev` against `recency_matched` | 11 won, 4 lost | 12 won, 4 lost |
| `jev` against `tail_plain` | 7 won, 10 lost | 6 won, 11 lost |
| `plugin_fallback` against `tail_plain` (same text, different prompt wording) | 13 won, 5 lost | 5 won, 10 lost |

Read the last row first: two arms that see the same text and differ only in prompt wording
moved 8 points in opposite directions across the two modes. That is the noise floor. With
it in mind:

1. **Jev's judgement is real and the digest built on it still lost.** Jev's marks beat the
   same number of marks handed out by recency in both modes. But a capsule written from the
   Jev digest recalled less than one written from the plain tail of the same size. The
   likely reason: a "summarize" turn survives as its first 400 characters, five of these
   seven sessions average 1,400 to 7,400 characters a turn, and no choice of turns recovers
   what clipping them throws away.
2. **What the writer reads was not the limit at 400 words.** The whole dialogue did no
   better than its last quarter. The capsule was full.
3. **One search is worth more than any of it.** Every arm gained 20 to 33 points. A
   session with no capsule and one search beat every closed-book capsule.

## Spending the capsule budget instead

| arm | words asked / written | closed-book | with one search |
|---|---|---|---|
| plain tail | 400 / 411 | 48.1% (50) | 68.3% (71) |
| plain tail | 1200 / 680 | 48.1% (50) | 65.4% (68) |
| `jev` | 1200 / 706 | 39.4% (41) | 63.5% (66) |
| whole dialogue | 400 / 408 | 46.2% (48) | 67.3% (70) |
| **whole dialogue** | **1200 / 824** | **58.7% (61)** | **75.0% (78)** |

Whole dialogue at 1,200 words, question by question: against what shipped, 26 won and 4
lost closed-book, 14 and 7 with a search. Against the plain tail at 400, 16 and 5, then 13
and 6. Against itself at 400 words, 16 and 3. A bigger budget did nothing for a writer that
had only read the tail, and reading everything did nothing for a writer held to 400 words.
It takes both. Reading the whole dialogue averaged 88,610 characters, about a cent.

This is what 0.14.0 ships: the whole dialogue (up to 300,000 characters), a 1,200-word
budget, no Jev pre-pass unless `HANDOFF_JEV=1`, and a Recovery section naming the session
and the search calls that work.

## Two things that were built, measured, and not shipped

| experiment | result |
|---|---|
| `digest_v2`: keep lines placed before any background, identifiers swept out of clipped text | 30.8% against 37.5% for the digest it was meant to replace; 5 won, 12 lost. With a search, 3 and 12 |
| A free regex-harvested list of the session's identifiers appended to the capsule | 49.0% against 48.1%; 4 won, 3 lost. Given to a session with **no** capsule it cost 13 points: 43.3% against 56.7% with one search, 4 won and 18 lost |

Both looked obviously right. Both are in `run_eval.py` so the numbers can be reproduced.

## Where the facts were

Of the 104 questions, the turn that best supported the answer was tool output for 48,
assistant text for 32 and the person's own words for 24. No arm reads tool output, because
the handoff plugin does not export it. The shipped configuration answered:

| the fact lived in | closed-book | with one search |
|---|---|---|
| the person's own words | 17 of 24 | 18 of 24 |
| assistant text | 22 of 32 | 26 of 32 |
| tool output | 22 of 48 | 34 of 48 |

Agents restate much of what their tools return, which is how a capsule that never saw tool
output still answers 22 of those 48. The search found 12 more, and it is the only way to
the rest.

## Cost

Jev: 13 requests, 7.8 s in total, for 7 sessions. The models: roughly two dollars for the
whole matrix, estimated from token counts, most of it the exam writer and the oracle each
reading every transcript once.

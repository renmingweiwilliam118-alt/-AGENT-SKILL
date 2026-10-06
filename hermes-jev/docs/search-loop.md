# Running a search as a loop

Most research turns are one search and a guess. The expensive model picks the query, opens
the first few results, and then decides — usually without being asked — whether to search
again. Three of those steps are decisions, and the third one is the one that goes wrong:
agents stop when they have something plausible, not when they have an answer.

`jev search` is the decision layer of a search loop. It does not search, and it does not
write. You bring the results; it answers three questions about them.

| Question | Type | What comes back |
|---|---|---|
| Which results are relevant, and which carry text aimed at an AI? | one score per result, batched into one request (plus a local, no-network screen on all of them) | `selected_ids`, ranked, plus `dropped_injection_ids` |
| Is this evidence enough to answer, or is another round needed? | yes/no with a confidence | `sufficiency`, `sufficient` |
| Which query should be run next? | pick one of the queries **you** wrote, or decline | `next_query`, `next_query_options` probabilities |

Jev cannot write a query — that is a property of the model, not a limitation of this
wrapper. So the loop is: you write two to five candidate queries, Jev picks one or says
none of them add anything.

## The four decisions, and what to do with each

| `decision` | When | What the agent does |
|---|---|---|
| `answer` | `sufficiency` ≥ 0.5 | Read `selected_ids` in order, write the answer. Do not search again. |
| `search_more` | Not enough, and a candidate query was picked | Run `next_query` verbatim and gate the new results with `round_index` + 1. |
| `propose_queries` | Not enough, and Jev declined every candidate (or none were offered) | Write new candidates from what is still missing. |
| `answer_from_what_we_have` | `round_index` reached `max_rounds` and the evidence is thin | Answer with what there is, and say what it does not cover. |
| `unknown` | Jev was not consulted at all | Decide yourself. |

`unknown` is the one to read carefully: it is not "the evidence is weak", it is "nothing was
asked". A key that has gone missing, a timeout, a sensitive question that was refused before
sending — all of those produce it, and `notes` says which.

## Two numbers that are not what they look like

- **`answerable`** is Jev's read on whether the *shortlist as a whole* contains the answer,
  on the same 0..1 scale as everything else. It is the memory filter's field, reused. When
  it is very low and `selected_ids` is empty, that is a real answer: the results are noise,
  search again.
- **`sufficiency` is `null` whenever the question was not asked**, which happens when no
  result survived the relevance screen or when the local screen flagged everything. A null
  is not a 0.0; `sufficient` is still `false` on the "everything was irrelevant" path,
  because Jev did read them.

## What was measured

A six-result round (rank, then sufficiency and the pick — two requests) against the live
TypeSafe endpoint, from this repo's machine:

- Wall clock for `jev search`: 1.54 s, 1.92 s, 2.26 s, 2.36 s, 1.55 s (median ~1.9 s).
- Per-request latency reported by the client: 917-1,475 ms.

Then the honest comparison, which is the one that matters: a frontier turn spent deciding
whether to search again costs more than that, and is usually the decision an agent gets
wrong by stopping early.

## Two defects the first live rounds found

Both are in the tests now, as reproductions.

1. **Everything irrelevant answered `unknown`.** Six Wikipedia results, all judged
   irrelevant, gave an empty `selected_ids` and `decision: unknown` — "Jev was not
   consulted" about a round where Jev had read all six. An agent following the table
   carries on alone; the honest answer was `search_more`. Now: when Jev judged the results
   and none passed, `sufficient` is `false`, no sufficiency question is asked about an empty
   shortlist (asking it would invite a coin flip and produce a number with nothing behind
   it), and the next-query pick is asked instead.
2. **Nothing was asked about the empty case at all.** The pick only happened when there were
   passages to send, so the one case where a new query matters most — nothing was relevant —
   was the one case that got no recommendation.

## When not to use it

- **You already know the answer.** The gate costs two requests and a second of latency.
- **The results hold anything the person marked private.** Send Jev the shapes, not the
  records: it needs the question and the snippets, not a customer list.
- **You need the search itself.** This is not a search engine and never fetches anything.

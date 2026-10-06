# Measuring a router on your own traffic

A router that has never been replayed against your own turns is a guess. This is how
the numbers in `CHANGELOG.md` were produced, and how to reproduce them.

## Why per-turn cost, not per-call price

An agent turn is not one API call. On this fleet the median turn is **8 API calls**
(p90 15.5, p99 35) because the model calls tools and the context is re-sent, and grows,
every time. Costing the first call understates a real turn by roughly an order of
magnitude and makes every model look equally cheap.

`jevkit.replay.loop_tokens` models it: context growing 8k → 40k tokens over the loop,
~700 output tokens per call. That is **192,000 input tokens and 5,600 output tokens**
for one median turn — **97% input**.

That ratio is the single most important number for picking models. The usual "blended"
price (80% input / 20% output) ranks models differently from an input-dominated agent
workload. Rank candidates by `192000 * input_price + 5600 * output_price`, not by a
blended figure, or you will pick a model that is cheap on paper and expensive in use.

## Replaying

Export your real turns to JSONL — one object per turn, `prompt` required:

```json
{"prompt": "...", "session_id": "...", "current": "openrouter:deepseek/deepseek-v4.1-flash", "context_tokens": 2500}
```

```bash
jev replay turns.jsonl --only-provider openrouter
```

You get the tier mix, which models were chosen, Jev's latency and confidence spread,
and — the part that decides whether to ship — the policy's cost against the baseline
those turns actually ran on.

Only Jev is called. No routed model is invoked, so replaying a few hundred turns costs
cents.

## A/B-ing a policy

`jevkit.replay.compare` runs the same turns under several configs. Cache `client.ask` by
question hash when variants differ only in their pools, so you pay for one Jev call per
turn rather than one per turn per variant.

The numbers that matter, in order:

1. **`cost.delta_pct`** — policy versus the baseline these turns really ran on. A router
   that raises the bill has to justify it with quality on the turns it upgraded.
2. **`tier_mix`** — if one tier holds most turns, the thresholds are wrong, not the traffic.
3. **`not_routed_template`** — turns skipped as cron/kanban boilerplate. On this fleet that
   is ~79% of all turns. They belong to profile configuration, not to a per-turn router.
4. **`confidence`** — a low median means the classifier cannot see the task. Fix what it is
   shown before touching any threshold.
5. **`jev_latency_ms`** — the router's own tax, paid on every turn.

## What this found here

Replaying 400 real turns, baseline `deepseek/deepseek-v4.1-flash` on every profile:

| policy | hard turns | cost vs baseline |
|---|---|---|
| hard pool led by `moonshotai/kimi-k3` | 18 | **+66.8%** |
| hard pool led by `z-ai/glm-5.3` | 18 | +28.8% |
| privacy-safe pools throughout | 18 | +19.5% |
| privacy-safe + `hard_needs_probability` 0.75 | 9 | **+8.4%** |

Three things that only showed up in replay:

- The most expensive model in the catalogue at the head of the hard pool cost more than
  every threshold change combined.
- **Privacy-safe pools were cheaper**, not more expensive — the assumed trade-off was not real.
- Raising the hard threshold from 0.6 to 0.75 halved the hard tier with no other change.

## Measure the prize before you optimize

Everything above is worthless if you have not answered "how much is being spent, on what?"
Pull the invoice by key and by model before writing a line of routing config:

- `openrouter.ai/activity/explore?metric=total_usage&dimension=model`
- `openrouter.ai/activity/explore?metric=total_usage&dimension=api_key_id&subgroup=model`

On the fleet this repo was built for, that took ten minutes and reordered every priority:

- Three API keys were **99.9%** of a $278/month bill.
- **57% of the bill was Claude models called at API rates** while a Claude Max subscription
  sat unused. One escalation-ladder rung was worth more than every routing change combined.
- The 41-profile agent fleet the router was written for spent **$0.127/month**. The router
  was being tuned against three ten-thousandths of the bill.
- Cache hit rate was **81.8%**, so switching models mid-session really does cost something —
  the opposite of what the per-call price table suggests.

None of that is visible from a price table, a benchmark, or a replay. Get the invoice first.

## A session that never ends is the most expensive thing you own

Before tuning which model answers, check how much conversation each answer carries.

On the deployment this repo was built for, two agents shared a $190/month run rate. The
cause was not the model and not the number of requests — it was **236,250 tokens per
request**. A 1,000,000-token context with a 0.50 compaction threshold lets a session grow
to 500k tokens before compacting and keeps a 100k tail, and one conversation had been
running for seventeen days and 2,255 messages. Every turn re-sent all of it.

Two fixes, in order of effect:

1. **End sessions on a schedule.** `hermes/scripts/nightly-handoff.py` writes a handoff
   capsule and closes each live conversation once a night. The next morning opens fresh
   and receives the capsule, so the agent knows what it was doing without carrying the
   transcript that proves it.
2. **Lower the context ceiling.** The compaction threshold is a fraction of
   `context_length`, so a 1M window is a decision to let sessions reach half a million
   tokens. 300k compacts at 150k.

Check it on your own deployment with one query:

```sql
select id, message_count from sessions where ended_at is null order by message_count desc limit 5;
```

If the top row is in the thousands, no amount of model routing will matter next to this.

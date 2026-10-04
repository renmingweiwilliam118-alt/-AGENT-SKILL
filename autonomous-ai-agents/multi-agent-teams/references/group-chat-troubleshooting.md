# Group-chat "bots aren't replying" diagnosis

Symptom: in a Bots group, every member shows `hit an error — HTTP 401:
Invalid token` (or similar) with `is working…` spinning. Your message reached
the room — forwarding, @-wake, and member spawn all fired — the failure is at
**reply generation** when the bot's model call is rejected. 401 = the
credential/quota layer, not the group logic.

## Read it in the right order
1. **Is it every member, same code?** All N bots 401ing identically =
   **shared credential / quota** problem, not a per-bot misconfig. These
   profiles typically share one key (`HERMES_CUSTOM_AGNES_API_KEY` from the
   root `.env` via each bot's `key_env`). A single-bot-only failure would point
   at that bot's config.
2. **Isolate single vs group:** run `hermes -p <one-bot> chat -q "正常"`.
   - Single bot **succeeds** but the group 401s → the group's **concurrency
     burst** (N inference calls at once) tripped a rate/quota gate. Fix:
     stop 6-way parallel replies; run through a coordinator that delegates
     (see `multi-agent-teams` SKILL.md). The token itself is fine.
   - Single bot **also 401s** → the token is genuinely bad: expired, rotated,
     or quota exhausted. Refresh the `.env` key. Flapping success↔401 on the
     single bot = quota/concurrency, not expiry.
3. **Confirm the exact status:** `grep -iE "401|invalid" $HERMES_HOME/logs/desktop.log`.
   Note the request ids; a `401 … not retryable` line means retrying won't help
   — it's a rejection, not a transient network blip.

## Why "works alone, fails in the group" happens
Group members are spawned as separate local profiles that each resolve the same
key. A solo CLI call is one inference request; a group turn is N requests in a
short window. Custom inference gateways commonly answer the burst with 401
(quota/concurrency) even when the token is valid — so a healthy-looking single
bot and a "broken" group can be the same token at different concurrency.

## What NOT to do
- Don't treat the 401 as a group/room bug and "recreate the group" — the
  mechanism already works (messages delivered, members woken).
- Don't write a per-bot key into each profile's `config.yaml` as "the fix"
  when a shared `.env` key is the source; resolve the shared credential
  (re-auth / refresh the root `.env`) unless you genuinely need per-bot keys.
- Don't claim a verified fix you didn't test: refresh the key, then re-send one
  group message and confirm a signed reply lands before calling it solved.

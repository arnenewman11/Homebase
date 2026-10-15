# Model policy

Match the model to the job, not the conversation. Set once, checked monthly by the steward, refined together.

| Tier | Like | Use for | Jobs |
|---|---|---|---|
| **Haiku** | The clerk | Frequent, rule-following, schema-guided work | Wall sync (hourly), Homebase refresh (5×/day), daily sort, roadmap status copy, weekly backup |
| **Sonnet** | The associate | Judgment, reviews, writing for you | Monday steward, Monday priorities review, finance tool review, opportunity search, intake from threads and roadmaps |
| **Opus** | The architect | Rare, high-leverage design | Planning sessions like the blueprint; never on a schedule |

## Habits

- Point helpers at the manifest instead of letting them search.
- Keep scheduled prompts short and fixed; every run pays for its instructions.
- New topic, new thread: long threads re-send their history every turn.
- Batch small asks into one message.

## How it is checked

- Every Homebase job writes `ops/<job>` with `model` at the end of each run.
- The steward flags any job running off-policy every Monday.
- On the first Monday of each month the steward adds a "Monthly model check" finding: what ran where, what looked weak, one suggested change. Approve or dismiss it in the System panel.
- Limit: Claude can't see the account's usage dashboard, so cost is estimated from what runs and how often, not measured.

## Change log

| Date | Change | Why |
|---|---|---|
| 2026-10-15 | All scheduled jobs moved off Opus: syncs/refresh/sort/backup → Haiku; reviews → Sonnet | Hourly Opus wall sync was the biggest token drain |

# Homebase manifest

Inventory of every part of the Homebase task system and what each part may touch.
Last updated: 2026-10-15 (Phase 2: inbox, daily sort, intake skill, backups). Helpers read this file instead of searching.

## Core

| Component | Role | Writes to |
|---|---|---|
| [Homebase](https://claude.ai/code/artifact/fadca305-7c93-4db1-8a1a-2d83f3d57244) | Canonical task store (`tasks`, `phases`, `areas`, `logs`) and phone view | Its own database |
| Living Room Dakboard (wall) | Wall view; reads the Google Sheet "Living Room Dakboard Feed" | Nothing |
| [Dakboard design canvas](https://claude.ai/code/artifact/00a68cda-57f1-4cde-a560-249b55e89052) | Mockups of the wall screens (not live data) | Nothing |
| [Blueprint (Claude Docs)](https://claude.ai/code/artifact/ac02e93d-14ae-474e-9704-66f6b5392107) | Design, schema and rules | Nothing |
| GitHub `arnenewman11/homebase` | Version history of pages, store snapshots, docs | — |

## Data model (Homebase database)

| Collection | Doc id | Key fields |
|---|---|---|
| `tasks` | `<prefix>-<source id>` e.g. `va-p1-01`, `cs-03`, `eb-14`, `hb-rewards` | title, detail, area, bucket, track, phase, order, type (should-do / want-do), status (inbox, todo, doing, waiting, parked, done, dropped), effort (S/M/L), due, nextStep, milestone, source, sourceRef, srcId, details, doneAt, createdAt, updatedAt, changedBy, demoSafe, mirror[] |
| `phases` | `<prefix>-<phase>` e.g. `va-p1` | area, track, name, label, order, milestone |
| `areas` | slug e.g. `card-sales` | name, bucket, prefix, sourceUrls, dbBacked, order, active |
| `logs` | `<taskId>-<yyyymmddhhmm>` | area, taskId, type (game, review, build, sale), date, fields |
| `garden` | area slug | leftOff, did, next, at |
| `feeds/*`, `state/*`, `plan/*`, `pending/*`, `quickDone/*`, `skips/*` | — | Unchanged page features |
| `va_*`, `arn_*`, `hbtasks` | — | **Retired** (kept for rollback; no longer read) |

Rules: no money amounts, balances or account details in tasks. `changedBy` is set on every write (you, router, steward, intake, migration).

## Areas and their plans

| Area slug | Name | Bucket | Plan | Plan has database |
|---|---|---|---|---|
| video-analysis | Video Analysis | Pickleball | [Video Analysis Roadmap](https://claude.ai/artifact/Bw2Jb85kbNKxwGsmQA68rg) | yes (status mirrored) |
| transition-zone | Transition Zone Class | Pickleball | [page](https://claude.ai/code/artifact/3f3ab2a8-afc6-4820-a698-2f79359eed57) | no |
| weekday-programming | Weekday Daytime Programming | Pickleball | [page](https://claude.ai/code/artifact/71f130b3-7b15-468d-873f-5eb6ecc7c788) | no |
| coaching-marketing | Coaching Marketing | Pickleball | [doc](https://claude.ai/code/artifact/693e7429-e042-413b-b021-6f51059d83f2) | no |
| card-sales | Card Sales (includes eBay Lots as track `ebay`) | Productivity | [Card Sales Roadmap](https://claude.ai/code/artifact/e6cdf650-213b-455e-8319-341304435f67), [eBay Lots Roadmap](https://claude.ai/code/artifact/3826c132-1940-4ff5-96f3-8beadefa4e9e) | yes (status mirrored) |
| advisor-path | Advisor path | Productivity | [doc](https://claude.ai/code/artifact/aa57b3ce-ef7d-4392-a943-2baa8e08639b) | no |
| water-wise | Water-Wise Yard Studio | Productivity | [doc](https://claude.ai/code/artifact/22c06970-73c4-4f19-bb0a-572a20cad3a1) | no |
| portfolio-twin | Portfolio Twin | Productivity | [page](https://claude.ai/code/artifact/0e534609-3502-4013-9807-eb49386040dc) | no |
| homebase | Homebase system | Productivity | Blueprint | no |
| money-admin | Money & admin | Productivity | — | no |
| arnfjall | Arnfjäll | Learn & Play | [Arnfjäll Roadmap](https://claude.ai/artifact/Kq7gv6mhnQ532qSfV5p2Cg) | yes (status mirrored) |
| ai-builder | AI Builder (28 steps; the 10 coarse ai-* items are dropped) | Learn & Play | [canvas](https://claude.ai/code/artifact/d34e8225-bdac-47e3-a3ba-0da4cde2c44b) | no |
| class-series | Class series (New to Pickleball) | Pickleball | — | no |
| ai-consulting | AI consulting (90-day test) | Productivity | — | no |

Archived as task sources (reference only): older eBay Lots copy (marked archived), career exploration docs, Top 20 Career Paths, Game Design Taste Test, Next Steps After 101 Flyer, Work Blend Planner, Weekday Class Survey, Card Decision Log, Finance App Decision, Arnfjäll Market Landscape, Pickleball Video Analysis Landscape, Daytime Market Scan, Transition Zone Glance Sheet.

The link claude.ai/artifact/T6Q1xGbQoY5bwtia4LXNDY is the same AI Builder Roadmap under a short URL.

## Scheduled tasks

| Name | When (Denver) | Model | Reads | Writes |
|---|---|---|---|---|
| Living Room Dakboard sync | hourly at :35 | Haiku | Calendar, Homebase db, Dakboard sheet `priorities` | Dakboard sheet `events`, `tasks`, `meta` |
| Homebase refresh | 5:59, 8:59, 11:59, 14:59, 17:59 | Haiku | Weather, Gmail, web | Homebase `feeds/*`; Gmail labels; Todoist bill tasks |
| Homebase daily sort | daily 6:26 | Haiku | Homebase inbox, Gmail label Homebase/To-do, personal calendar (read) | Homebase `tasks` (inbox items only), `sort/state` |
| Roadmap status mirror | daily 6:47 | Haiku | Homebase `tasks` | Status fields in the 4 database roadmaps |
| Weekly priorities review | Mon 8:50 | Sonnet | Dakboard sheet, Homebase db | Message to you |
| Weekly finance tool review | Mon 7:51 | Sonnet | Drive, Gmail, Todoist (read) | "Finance Tool Review Log" doc |
| Weekly Part-Time Opportunity Search | Mon 8:00 | Sonnet | Job boards, web | Project log |
| Homebase weekly backup | Sun 21:46 | Haiku | Homebase db | Drive Homebase/Backups (JSON + CSV, keeps 8) |
| Arnfjäll Roadmap sync | — | Haiku | — | **Paused** (replaced by the mirror) |
| Roadmap write-back from Homebase | — | Haiku | — | **Paused** (Homebase writes its own store now) |
| Reminders (goals & measuring sticks ×3, day-tracking questions) | one-time | — | — | Message to you |

## Connectors: allowed for unattended runs

| Connector | Allowed on its own | Always waits for you |
|---|---|---|
| Gmail | Read; apply Homebase labels (refresh only) | Send, draft, reply, forward, delete |
| Google Calendar | Read; create draft events | Invites, deletes, edits to existing events |
| Google Drive | Write exports to the Homebase folder; read the blueprint | Share, trash, other folders |
| Google Sheets | Dakboard feed tabs `events`, `tasks`, `meta` | Sharing, `priorities` tab |
| Todoist | Add "Pay … bill" tasks (refresh only) | Everything else |

Open item: every scheduled task currently has all connectors attached. Trim each task's connectors in its settings to match this table.

## Security notes

- The Dakboard feed sheet is "anyone with the link can view" because DAKboard can only display published sheets. It holds calendar event titles and task titles; no locations, attendees or amounts.
- Artifacts are private to you.

## Capture

| Input | How | Lands as |
|---|---|---|
| Quick add (Homebase, Today screen) | Type, or dictate with the keyboard mic | `status: inbox`, `source: quick-add` |
| Gmail | Apply label **Homebase/To-do** | `em-<thread id>`, inbox, via the daily sort |
| Calendar | Automatic, conservative (max 2 per day) | `cal-<event id>`, inbox, always needs your tap |
| Any chat | "Add these to Homebase" (skill `add-to-homebase`) | Filed directly, or inbox when unsure |

The daily sort files confident items (`changedBy: router`) and leaves unsure ones in the inbox with `suggestedArea` for a one-tap confirm.

## Decisions log

- 2026-10-15: Todoist wall bridge dropped. The Dakboard stays sheet-based; check-offs happen in Homebase. Revisit if a touch add-on is bought.

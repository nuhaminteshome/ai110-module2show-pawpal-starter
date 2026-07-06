# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

## Sample Output

```
Welcome to PawPal+, Alex!

========== Today's Schedule ==========

=== Daily Schedule: 2026-07-01 ===
  07:00 — Morning Walk (30 min) [priority: high] [pending]
  08:00 — Feeding (10 min) [priority: high] [pending]
  09:00 — Medication (5 min) [priority: high] [pending]
  15:00 — Playtime (20 min) [priority: medium] [pending]
  18:00 — Grooming (15 min) [priority: low] [pending]

=== Schedule Reasoning ===
Tasks ordered by priority for 2026-07-01:
  - [HIGH] Morning Walk for Luna (30 min)
  - [HIGH] Feeding for Luna (10 min)
  - [HIGH] Medication for Mochi (5 min)
  - [MEDIUM] Playtime for Mochi (20 min)
  - [LOW] Grooming for Mochi (15 min)
```
## 🧪 Testing PawPal+

Run the full test suite from the project root:

```bash
python -m pytest
```

Run with verbose output to see each test name:

```bash
python -m pytest -v
```

The suite (`tests/test_pawpal.py`) covers the core object model (`Task`, `Pet`, `PetOwner`) plus the three scheduling behaviors that matter most for correctness:

- **Sorting correctness** — `generate_schedule()` orders tasks high → medium → low priority (with unrecognized priority values sorted last instead of erroring), and `sort_by_time()` re-sorts chronologically by preferred time, pushing tasks with no time set to the end.
- **Recurrence logic** — completing a `"daily"` task creates a new pending task due the next day, completing a `"weekly"` task creates one due a week later, a missing `due_date` falls back to today, and tasks with an unrecognized frequency (or no owning pet) complete without creating a bad or duplicate successor.
- **Conflict detection** — `find_conflicts()` flags tasks sharing the same time slot for both the same pet and different pets, ignores tasks with no time set, and `get_conflict_warnings()` labels each conflict as `[same pet]` or `[different pets]` without raising on malformed data.

Sample test output:

```
============================= test session starts =============================
platform win32 -- Python 3.13.5, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\nuham\Downloads\CodePath - AI110\ai110-module2show-pawpal-starter
plugins: anyio-4.14.0
collected 24 items

tests\test_pawpal.py ........................                            [100%]

============================= 24 passed in 0.06s ==============================
```

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `DailySchedule.generate_schedule()`, `DailySchedule.sort_by_time()` | `generate_schedule()` sorts tasks by priority (high → medium → low). `sort_by_time()` re-sorts the same list by each task's preferred time, earliest first, pushing tasks with no time set to the end. |
| Filtering | `PetOwner.filter_tasks(completed=None, pet_name=None)` | Returns tasks across all pets, optionally narrowed by completion status and/or by pet name. Both filters are optional and combine with AND logic. |
| Conflict handling | `DailySchedule.find_conflicts()`, `DailySchedule.get_conflict_warnings()`, `DailySchedule.display_conflicts()` | `find_conflicts()` groups tasks by their time slot and flags any slot with more than one task. `get_conflict_warnings()` turns those groups into readable warning messages (labeling each as a "same pet" or "different pets" conflict) and never raises, even if scheduling data is malformed. `display_conflicts()` prints the warnings to the terminal. Note: conflicts are only detected on exact time matches, not overlapping durations — see `reflection.md` for that tradeoff. |
| Recurring tasks | `Task.mark_complete()` | When a "daily" or "weekly" task is marked complete, this method automatically creates a new, pending `Task` instance for the next occurrence. The next due date is calculated with `datetime.timedelta` (+1 day for daily, +7 days for weekly) and the new task is added back to the same pet. |

## 📸 Demo Walkthrough

### Main UI features

The Streamlit app (`app.py`) lets a user:

- Enter owner and pet info (name, pet name, species) and save it
- Add tasks to the active pet (title, duration, priority, preferred time)
- View current tasks in a table, filterable by **All / Pending / Completed**
- Generate a daily schedule, optionally sorted by time instead of priority
- See any scheduling conflicts flagged before the schedule itself, along with the plain-language reasoning behind the task order

### Example workflow

1. Save an owner ("Alex") and a pet ("Luna the Dog").
2. Add a few tasks for Luna — e.g. "Morning Walk" (high priority, 07:00) and "Feeding" (high priority, 08:00).
3. Check the tasks table to confirm they were added, then switch the filter to "Pending" to confirm both show up.
4. Click "Generate Schedule" to see today's plan ordered by priority, with the reasoning explained underneath.
5. Toggle "Sort by time" to re-order the same schedule chronologically instead.
6. If two tasks land on the same time slot, the conflict is called out above the schedule — as an error if it's the same pet double-booked, or a warning if it's two different pets.

### Key Scheduler behaviors shown

- **Sorting** — `generate_schedule()` orders tasks by priority (high → medium → low); `sort_by_time()` re-orders the same list chronologically.
- **Conflict warnings** — `find_conflicts()` / `get_conflict_warnings()` catch tasks sharing a time slot and label each as a same-pet or different-pets clash.
- **Recurrence** — `mark_complete()` on a daily/weekly task automatically creates the next occurrence with the correct due date.

### Sample CLI output (`python main.py`)

```
Welcome to PawPal+, Alex!

========== Schedule sorted by PRIORITY ==========

=== Daily Schedule: 2026-07-01 ===
  08:00 — Feeding (10 min) [priority: high] [done]
  07:00 — Morning Walk (30 min) [priority: high] [pending]
  08:00 — Feeding (10 min) [priority: high] [pending]
  09:00 — Medication (5 min) [priority: high] [pending]
  07:00 — Training Session (15 min) [priority: medium] [pending]
  15:00 — Playtime (20 min) [priority: medium] [pending]
  09:00 — Vet Check-in Call (10 min) [priority: low] [pending]
  18:00 — Grooming (15 min) [priority: low] [done]
  18:00 — Grooming (15 min) [priority: low] [pending]

=== Schedule Reasoning ===
Tasks ordered by priority for 2026-07-01:
  - [HIGH] Feeding for Luna (10 min)
  - [HIGH] Morning Walk for Luna (30 min)
  - [HIGH] Feeding for Luna (10 min)
  - [HIGH] Medication for Mochi (5 min)
  - [MEDIUM] Training Session for Luna (15 min)
  - [MEDIUM] Playtime for Mochi (20 min)
  - [LOW] Vet Check-in Call for Luna (10 min)
  - [LOW] Grooming for Mochi (15 min)
  - [LOW] Grooming for Mochi (15 min)

========== Schedule sorted by TIME ==========

=== Daily Schedule: 2026-07-01 ===
  07:00 — Morning Walk (30 min) [priority: high] [pending]
  07:00 — Training Session (15 min) [priority: medium] [pending]
  08:00 — Feeding (10 min) [priority: high] [done]
  08:00 — Feeding (10 min) [priority: high] [pending]
  09:00 — Medication (5 min) [priority: high] [pending]
  09:00 — Vet Check-in Call (10 min) [priority: low] [pending]
  15:00 — Playtime (20 min) [priority: medium] [pending]
  18:00 — Grooming (15 min) [priority: low] [done]
  18:00 — Grooming (15 min) [priority: low] [pending]

=== Scheduling Conflicts ===
  Warning: scheduling conflict at 07:00 [same pet]: Morning Walk (Luna), Training Session (Luna)
  Warning: scheduling conflict at 08:00 [same pet]: Feeding (Luna), Feeding (Luna)
  Warning: scheduling conflict at 09:00 [different pets]: Medication (Mochi), Vet Check-in Call (Luna)
  Warning: scheduling conflict at 18:00 [same pet]: Grooming (Mochi), Grooming (Mochi)

========== Pending Tasks ==========
  07:00 — Morning Walk for Luna
  07:00 — Training Session for Luna
  09:00 — Vet Check-in Call for Luna
  08:00 — Feeding for Luna
  09:00 — Medication for Mochi
  15:00 — Playtime for Mochi
  18:00 — Grooming for Mochi

========== Completed Tasks ==========
  08:00 — Feeding for Luna
  18:00 — Grooming for Mochi

========== Mochi's Tasks ==========
  18:00 — Grooming (low)
  09:00 — Medication (high)
  15:00 — Playtime (medium)
  18:00 — Grooming (low)

========== Due Dates (verifying timedelta rollover) ==========
  Feeding for Luna [daily] due 2026-07-01 [done]
  Morning Walk for Luna [daily] due 2026-07-01 [pending]
  Training Session for Luna [daily] due 2026-07-01 [pending]
  Vet Check-in Call for Luna [daily] due 2026-07-01 [pending]
  Feeding for Luna [daily] due 2026-07-02 [pending]
  Grooming for Mochi [weekly] due 2026-07-01 [done]
  Medication for Mochi [daily] due 2026-07-01 [pending]
  Playtime for Mochi [daily] due 2026-07-01 [pending]
  Grooming for Mochi [weekly] due 2026-07-08 [pending]
```

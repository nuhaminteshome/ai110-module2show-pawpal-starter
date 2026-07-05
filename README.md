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

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `DailySchedule.generate_schedule()`, `DailySchedule.sort_by_time()` | `generate_schedule()` sorts tasks by priority (high → medium → low). `sort_by_time()` re-sorts the same list by each task's preferred time, earliest first, pushing tasks with no time set to the end. |
| Filtering | `PetOwner.filter_tasks(completed=None, pet_name=None)` | Returns tasks across all pets, optionally narrowed by completion status and/or by pet name. Both filters are optional and combine with AND logic. |
| Conflict handling | `DailySchedule.find_conflicts()`, `DailySchedule.get_conflict_warnings()`, `DailySchedule.display_conflicts()` | `find_conflicts()` groups tasks by their time slot and flags any slot with more than one task. `get_conflict_warnings()` turns those groups into readable warning messages (labeling each as a "same pet" or "different pets" conflict) and never raises, even if scheduling data is malformed. `display_conflicts()` prints the warnings to the terminal. Note: conflicts are only detected on exact time matches, not overlapping durations — see `reflection.md` for that tradeoff. |
| Recurring tasks | `Task.mark_complete()` | When a "daily" or "weekly" task is marked complete, this method automatically creates a new, pending `Task` instance for the next occurrence. The next due date is calculated with `datetime.timedelta` (+1 day for daily, +7 days for weekly) and the new task is added back to the same pet. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->

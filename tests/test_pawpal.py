import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from datetime import date, timedelta

from pawpal_system import Task, Pet, PetOwner, DailySchedule


# --- Task Tests ---

def test_task_creation():
    task = Task(type_of_task="Walk", priority_level="high", duration=30)
    assert task.type_of_task == "Walk"
    assert task.priority_level == "high"
    assert task.duration == 30
    assert task.completed == False


def test_task_mark_complete():
    task = Task(type_of_task="Feeding", priority_level="medium", duration=10)
    task.mark_complete()
    assert task.completed == True


def test_task_edit():
    task = Task(type_of_task="Walk", priority_level="low", duration=20)
    task.edit_task(priority_level="high", duration=45)
    assert task.priority_level == "high"
    assert task.duration == 45


# --- Pet Tests ---

def test_pet_add_task():
    pet = Pet(name="Luna", pet_type="Dog")
    task = Task(type_of_task="Walk", priority_level="high", duration=30)
    pet.add_task(task)
    assert task in pet.tasks
    assert task.pet_name == "Luna"


def test_pet_delete_task():
    pet = Pet(name="Luna", pet_type="Dog")
    task = Task(type_of_task="Walk", priority_level="high", duration=30)
    pet.add_task(task)
    pet.delete_task(task)
    assert task not in pet.tasks


def test_pet_update_info():
    pet = Pet(name="Luna", pet_type="Dog")
    pet.update_pet_info(name="Luna Bear", pet_type="Husky")
    assert pet.name == "Luna Bear"
    assert pet.pet_type == "Husky"


# --- PetOwner Tests ---

def test_owner_add_pet():
    owner = PetOwner("Alex")
    pet = Pet(name="Luna", pet_type="Dog")
    owner.add_pet(pet)
    assert pet in owner.pets


def test_owner_get_all_tasks():
    owner = PetOwner("Alex")
    luna = Pet(name="Luna", pet_type="Dog")
    mochi = Pet(name="Mochi", pet_type="Cat")
    luna.add_task(Task(type_of_task="Walk", priority_level="high", duration=30))
    mochi.add_task(Task(type_of_task="Feeding", priority_level="medium", duration=10))
    owner.add_pet(luna)
    owner.add_pet(mochi)
    assert len(owner.get_all_tasks()) == 2


# --- DailySchedule Tests ---

def test_schedule_sorted_by_priority():
    owner = PetOwner("Alex")
    luna = Pet(name="Luna", pet_type="Dog")
    luna.add_task(Task(type_of_task="Grooming", priority_level="low", duration=15))
    luna.add_task(Task(type_of_task="Meds", priority_level="high", duration=5))
    luna.add_task(Task(type_of_task="Walk", priority_level="medium", duration=30))
    owner.add_pet(luna)

    schedule = DailySchedule(date="2026-07-01", owner=owner)
    schedule.generate_schedule()

    priorities = [t.priority_level for t in schedule.scheduled_tasks]
    assert priorities == ["high", "medium", "low"]


def test_schedule_reasoning_not_empty():
    owner = PetOwner("Alex")
    luna = Pet(name="Luna", pet_type="Dog")
    luna.add_task(Task(type_of_task="Walk", priority_level="high", duration=30))
    owner.add_pet(luna)

    schedule = DailySchedule(date="2026-07-01", owner=owner)
    schedule.generate_schedule()
    assert schedule.reasoning != ""


# --- Sorting Correctness ---

def test_sort_by_time_chronological_order():
    owner = PetOwner("Alex")
    luna = Pet(name="Luna", pet_type="Dog")
    luna.add_task(Task(type_of_task="Playtime", priority_level="medium", duration=20, time="15:00"))
    luna.add_task(Task(type_of_task="Feeding", priority_level="high", duration=10, time="08:00"))
    luna.add_task(Task(type_of_task="Walk", priority_level="high", duration=30, time="07:00"))
    owner.add_pet(luna)

    schedule = DailySchedule(date="2026-07-01", owner=owner)
    schedule.generate_schedule()
    schedule.sort_by_time()

    times = [t.time for t in schedule.scheduled_tasks]
    assert times == ["07:00", "08:00", "15:00"]


def test_sort_by_time_pushes_untimed_tasks_to_end():
    owner = PetOwner("Alex")
    luna = Pet(name="Luna", pet_type="Dog")
    luna.add_task(Task(type_of_task="No Time Task", priority_level="low", duration=5, time=""))
    luna.add_task(Task(type_of_task="Feeding", priority_level="high", duration=10, time="08:00"))
    owner.add_pet(luna)

    schedule = DailySchedule(date="2026-07-01", owner=owner)
    schedule.generate_schedule()
    schedule.sort_by_time()

    assert schedule.scheduled_tasks[-1].type_of_task == "No Time Task"


def test_schedule_sorted_by_unknown_priority_falls_to_end():
    owner = PetOwner("Alex")
    luna = Pet(name="Luna", pet_type="Dog")
    luna.add_task(Task(type_of_task="Mystery", priority_level="urgent", duration=5))
    luna.add_task(Task(type_of_task="Walk", priority_level="high", duration=30))
    owner.add_pet(luna)

    schedule = DailySchedule(date="2026-07-01", owner=owner)
    schedule.generate_schedule()

    assert schedule.scheduled_tasks[-1].type_of_task == "Mystery"


# --- Recurrence Logic ---

def test_mark_complete_daily_creates_next_day_task():
    luna = Pet(name="Luna", pet_type="Dog")
    today = date(2026, 7, 1)
    task = Task(type_of_task="Feeding", priority_level="high", duration=10,
                frequency="daily", due_date=today)
    luna.add_task(task)

    task.mark_complete()

    assert task.completed is True
    assert len(luna.tasks) == 2
    next_task = luna.tasks[1]
    assert next_task.due_date == today + timedelta(days=1)
    assert next_task.completed is False
    assert next_task.type_of_task == "Feeding"


def test_mark_complete_weekly_creates_task_one_week_later():
    mochi = Pet(name="Mochi", pet_type="Cat")
    today = date(2026, 7, 1)
    task = Task(type_of_task="Grooming", priority_level="low", duration=15,
                frequency="weekly", due_date=today)
    mochi.add_task(task)

    task.mark_complete()

    next_task = mochi.tasks[1]
    assert next_task.due_date == today + timedelta(weeks=1)


def test_mark_complete_without_due_date_defaults_to_today():
    luna = Pet(name="Luna", pet_type="Dog")
    task = Task(type_of_task="Feeding", priority_level="high", duration=10, frequency="daily")
    luna.add_task(task)

    task.mark_complete()

    next_task = luna.tasks[1]
    assert next_task.due_date == date.today() + timedelta(days=1)


def test_mark_complete_unknown_frequency_creates_no_recurrence():
    luna = Pet(name="Luna", pet_type="Dog")
    task = Task(type_of_task="Vet Visit", priority_level="medium", duration=60, frequency="monthly")
    luna.add_task(task)

    task.mark_complete()

    assert task.completed is True
    assert len(luna.tasks) == 1  # no successor created for an unsupported frequency


def test_mark_complete_without_pet_creates_no_recurrence():
    # Task never added to a pet, so _pet is None; mark_complete should not raise.
    task = Task(type_of_task="Feeding", priority_level="high", duration=10, frequency="daily")

    task.mark_complete()

    assert task.completed is True


# --- Conflict Detection ---

def test_find_conflicts_flags_same_time_different_pets():
    owner = PetOwner("Alex")
    luna = Pet(name="Luna", pet_type="Dog")
    mochi = Pet(name="Mochi", pet_type="Cat")
    luna.add_task(Task(type_of_task="Walk", priority_level="high", duration=30, time="09:00"))
    mochi.add_task(Task(type_of_task="Medication", priority_level="high", duration=5, time="09:00"))
    owner.add_pet(luna)
    owner.add_pet(mochi)

    schedule = DailySchedule(date="2026-07-01", owner=owner)
    schedule.generate_schedule()

    conflicts = schedule.find_conflicts()
    assert "09:00" in conflicts
    assert len(conflicts["09:00"]) == 2


def test_find_conflicts_flags_same_time_same_pet():
    owner = PetOwner("Alex")
    luna = Pet(name="Luna", pet_type="Dog")
    luna.add_task(Task(type_of_task="Walk", priority_level="high", duration=30, time="07:00"))
    luna.add_task(Task(type_of_task="Training", priority_level="medium", duration=15, time="07:00"))
    owner.add_pet(luna)

    schedule = DailySchedule(date="2026-07-01", owner=owner)
    schedule.generate_schedule()

    conflicts = schedule.find_conflicts()
    assert "07:00" in conflicts
    assert len(conflicts["07:00"]) == 2


def test_find_conflicts_ignores_distinct_times():
    owner = PetOwner("Alex")
    luna = Pet(name="Luna", pet_type="Dog")
    luna.add_task(Task(type_of_task="Walk", priority_level="high", duration=30, time="07:00"))
    luna.add_task(Task(type_of_task="Feeding", priority_level="high", duration=10, time="08:00"))
    owner.add_pet(luna)

    schedule = DailySchedule(date="2026-07-01", owner=owner)
    schedule.generate_schedule()

    assert schedule.find_conflicts() == {}


def test_find_conflicts_ignores_tasks_without_time():
    owner = PetOwner("Alex")
    luna = Pet(name="Luna", pet_type="Dog")
    luna.add_task(Task(type_of_task="Walk", priority_level="high", duration=30, time=""))
    luna.add_task(Task(type_of_task="Feeding", priority_level="high", duration=10, time=""))
    owner.add_pet(luna)

    schedule = DailySchedule(date="2026-07-01", owner=owner)
    schedule.generate_schedule()

    assert schedule.find_conflicts() == {}


def test_get_conflict_warnings_labels_same_pet_vs_different_pets():
    owner = PetOwner("Alex")
    luna = Pet(name="Luna", pet_type="Dog")
    mochi = Pet(name="Mochi", pet_type="Cat")
    luna.add_task(Task(type_of_task="Walk", priority_level="high", duration=30, time="07:00"))
    luna.add_task(Task(type_of_task="Training", priority_level="medium", duration=15, time="07:00"))
    mochi.add_task(Task(type_of_task="Medication", priority_level="high", duration=5, time="09:00"))
    luna.add_task(Task(type_of_task="Vet Call", priority_level="low", duration=10, time="09:00"))
    owner.add_pet(luna)
    owner.add_pet(mochi)

    schedule = DailySchedule(date="2026-07-01", owner=owner)
    schedule.generate_schedule()

    warnings = schedule.get_conflict_warnings()
    assert any("[same pet]" in w and "07:00" in w for w in warnings)
    assert any("[different pets]" in w and "09:00" in w for w in warnings)


def test_get_conflict_warnings_returns_empty_list_when_no_conflicts():
    owner = PetOwner("Alex")
    luna = Pet(name="Luna", pet_type="Dog")
    luna.add_task(Task(type_of_task="Walk", priority_level="high", duration=30, time="07:00"))
    owner.add_pet(luna)

    schedule = DailySchedule(date="2026-07-01", owner=owner)
    schedule.generate_schedule()

    assert schedule.get_conflict_warnings() == []

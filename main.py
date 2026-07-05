from datetime import date
from pawpal_system import Task, Pet, PetOwner, DailySchedule

TODAY = date(2026, 7, 1)

# --- Setup Owner ---
owner = PetOwner()
owner.add_name("Alex")

# --- Create Pets ---
luna = Pet(name="Luna", pet_type="Dog")
mochi = Pet(name="Mochi", pet_type="Cat")

owner.add_pet(luna)
owner.add_pet(mochi)

# --- Add Tasks to Luna (Dog), added out of time order on purpose ---
luna.add_task(Task(
    type_of_task="Feeding",
    priority_level="high",
    duration=10,
    time="08:00",
    frequency="daily",
    due_date=TODAY
))

luna.add_task(Task(
    type_of_task="Morning Walk",
    priority_level="high",
    duration=30,
    time="07:00",
    frequency="daily",
    due_date=TODAY
))

# --- Add Tasks to Mochi (Cat), also added out of time order ---
mochi.add_task(Task(
    type_of_task="Grooming",
    priority_level="low",
    duration=15,
    time="18:00",
    frequency="weekly",
    due_date=TODAY
))

mochi.add_task(Task(
    type_of_task="Medication",
    priority_level="high",
    duration=5,
    time="09:00",
    frequency="daily",
    due_date=TODAY
))

mochi.add_task(Task(
    type_of_task="Playtime",
    priority_level="medium",
    duration=20,
    time="15:00",
    frequency="daily",
    due_date=TODAY
))

# --- Tasks added deliberately to create scheduling conflicts ---
luna.add_task(Task(
    type_of_task="Training Session",
    priority_level="medium",
    duration=15,
    time="07:00",          # same time as Luna's own Morning Walk -> same-pet conflict
    frequency="daily",
    due_date=TODAY
))

luna.add_task(Task(
    type_of_task="Vet Check-in Call",
    priority_level="low",
    duration=10,
    time="09:00",          # same time as Mochi's Medication -> cross-pet conflict
    frequency="daily",
    due_date=TODAY
))

# Mark tasks complete so filtering by status has something to show, and to
# demonstrate the next occurrence being auto-created with the correct due date
luna.tasks[0].mark_complete()      # daily -> next due_date should be TODAY + 1 day
mochi.tasks[0].mark_complete()     # weekly -> next due_date should be TODAY + 7 days

# --- Generate Schedule (sorted by priority) ---
schedule = DailySchedule(date="2026-07-01", owner=owner)
schedule.generate_schedule()

print(f"\nWelcome to PawPal+, {owner.name_of_owner}!")

print("\n========== Schedule sorted by PRIORITY ==========")
schedule.display_schedule()
schedule.display_reasoning()

# --- Re-sort the same schedule by time ---
schedule.sort_by_time()
print("\n========== Schedule sorted by TIME ==========")
schedule.display_schedule()

# --- Detect scheduling conflicts (same time, same or different pets) ---
schedule.display_conflicts()

# --- Filter tasks by completion status ---
print("\n========== Pending Tasks ==========")
for task in owner.filter_tasks(completed=False):
    print(f"  {task.time} — {task.type_of_task} for {task.pet_name}")

print("\n========== Completed Tasks ==========")
for task in owner.filter_tasks(completed=True):
    print(f"  {task.time} — {task.type_of_task} for {task.pet_name}")

# --- Filter tasks by pet name ---
print("\n========== Mochi's Tasks ==========")
for task in owner.filter_tasks(pet_name="Mochi"):
    print(f"  {task.time} — {task.type_of_task} ({task.priority_level})")

# --- Verify recurring due dates advance correctly ---
print("\n========== Due Dates (verifying timedelta rollover) ==========")
for task in owner.get_all_tasks():
    status = "done" if task.completed else "pending"
    print(f"  {task.type_of_task} for {task.pet_name} [{task.frequency}] "
          f"due {task.due_date} [{status}]")

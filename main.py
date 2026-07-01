from pawpal_system import Task, Pet, PetOwner, DailySchedule

# --- Setup Owner ---
owner = PetOwner()
owner.add_name("Alex")

# --- Create Pets ---
luna = Pet(name="Luna", pet_type="Dog")
mochi = Pet(name="Mochi", pet_type="Cat")

owner.add_pet(luna)
owner.add_pet(mochi)

# --- Add Tasks to Luna (Dog) ---
luna.add_task(Task(
    type_of_task="Morning Walk",
    priority_level="high",
    duration=30,
    time="07:00",
    frequency="daily"
))

luna.add_task(Task(
    type_of_task="Feeding",
    priority_level="high",
    duration=10,
    time="08:00",
    frequency="daily"
))

# --- Add Tasks to Mochi (Cat) ---
mochi.add_task(Task(
    type_of_task="Medication",
    priority_level="high",
    duration=5,
    time="09:00",
    frequency="daily"
))

mochi.add_task(Task(
    type_of_task="Playtime",
    priority_level="medium",
    duration=20,
    time="15:00",
    frequency="daily"
))

mochi.add_task(Task(
    type_of_task="Grooming",
    priority_level="low",
    duration=15,
    time="18:00",
    frequency="weekly"
))

# --- Generate and Display Schedule ---
schedule = DailySchedule(date="2026-07-01", owner=owner)
schedule.generate_schedule()

print(f"\nWelcome to PawPal+, {owner.name_of_owner}!")
print("\n========== Today's Schedule ==========")
schedule.display_schedule()
schedule.display_reasoning()

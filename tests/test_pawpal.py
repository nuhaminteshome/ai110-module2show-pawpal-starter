import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

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

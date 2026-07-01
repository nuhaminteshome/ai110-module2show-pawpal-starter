from dataclasses import dataclass, field
from typing import List


@dataclass
class Task:
    type_of_task: str
    priority_level: str       # "high", "medium", or "low"
    duration: int             # in minutes
    pet_name: str = ""
    time: str = ""            # preferred time e.g. "08:00"
    frequency: str = "daily"  # "daily", "weekly", etc.
    completed: bool = False

    def edit_task(self, type_of_task: str = None, priority_level: str = None,
                  duration: int = None, time: str = None, frequency: str = None):
        """Update one or more fields on this task."""
        if type_of_task:
            self.type_of_task = type_of_task
        if priority_level:
            self.priority_level = priority_level
        if duration is not None:
            self.duration = duration
        if time:
            self.time = time
        if frequency:
            self.frequency = frequency

    def mark_complete(self):
        """Mark this task as completed."""
        self.completed = True


@dataclass
class Pet:
    name: str
    pet_type: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        """Add a task to this pet and tag it with the pet's name."""
        task.pet_name = self.name
        self.tasks.append(task)

    def delete_task(self, task: Task):
        """Remove a task from this pet's task list."""
        if task in self.tasks:
            self.tasks.remove(task)

    def update_pet_info(self, name: str = None, pet_type: str = None):
        """Update the pet's name or type."""
        if name:
            self.name = name
        if pet_type:
            self.pet_type = pet_type


class PetOwner:
    def __init__(self, name: str = ""):
        self.name_of_owner = name
        self.pets: List[Pet] = []

    def add_name(self, name: str):
        """Set the owner's name."""
        self.name_of_owner = name

    def add_pet(self, pet: Pet):
        """Add a pet to the owner's list of pets."""
        self.pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        """Collect and return all tasks across every pet."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks


class DailySchedule:
    def __init__(self, date: str, owner: PetOwner):
        self.date = date
        self.owner = owner
        self.reasoning = ""
        self.scheduled_tasks: List[Task] = []

    def generate_schedule(self):
        """Sort all tasks by priority and build the reasoning string."""
        all_tasks = self.owner.get_all_tasks()
        priority_order = {"high": 0, "medium": 1, "low": 2}
        self.scheduled_tasks = sorted(
            all_tasks,
            key=lambda t: priority_order.get(t.priority_level.lower(), 3)
        )
        self.reasoning = self._build_reasoning()

    def _build_reasoning(self) -> str:
        """Build a human-readable explanation of the schedule order."""
        if not self.scheduled_tasks:
            return "No tasks to schedule."
        lines = [f"Tasks ordered by priority for {self.date}:"]
        for task in self.scheduled_tasks:
            lines.append(
                f"  - [{task.priority_level.upper()}] {task.type_of_task} "
                f"for {task.pet_name} ({task.duration} min)"
            )
        return "\n".join(lines)

    def display_schedule(self):
        """Print the daily schedule to the terminal."""
        if not self.scheduled_tasks:
            print("No schedule generated yet. Call generate_schedule() first.")
            return
        print(f"\n=== Daily Schedule: {self.date} ===")
        for task in self.scheduled_tasks:
            time_str = task.time if task.time else "??:??"
            status = "done" if task.completed else "pending"
            print(f"  {time_str} — {task.type_of_task} ({task.duration} min) [priority: {task.priority_level}] [{status}]")

    def display_reasoning(self):
        """Print the reasoning behind the generated schedule."""
        print("\n=== Schedule Reasoning ===")
        print(self.reasoning if self.reasoning else "No reasoning available yet.")

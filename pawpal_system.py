from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import List, Optional

FREQUENCY_INTERVALS = {
    "daily": timedelta(days=1),
    "weekly": timedelta(weeks=1),
}


@dataclass
class Task:
    type_of_task: str
    priority_level: str       # "high", "medium", or "low"
    duration: int             # in minutes
    pet_name: str = ""
    time: str = ""            # preferred time e.g. "08:00"
    frequency: str = "daily"  # "daily", "weekly", etc.
    completed: bool = False
    due_date: Optional[date] = None
    # Back-reference to the owning Pet, used to auto-create the next
    # recurring occurrence. Excluded from repr/eq so Task<->Pet don't recurse.
    _pet: Optional["Pet"] = field(default=None, repr=False, compare=False)

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
        """Mark this task as completed, and auto-create the next occurrence
        if it's a recurring task.

        Algorithm: looks up this task's frequency ("daily"/"weekly") in
        FREQUENCY_INTERVALS to get the matching timedelta, then computes
        next_due = base_date + interval, where base_date is this task's
        due_date (or today if it has none). A new pending Task is created
        with that due date and added back to the same pet. Non-recurring
        tasks, or tasks with no owning pet, are just marked complete with
        no further side effects.

        Time complexity: O(1).
        """
        self.completed = True
        interval = FREQUENCY_INTERVALS.get(self.frequency)
        if interval is not None and self._pet is not None:
            base_date = self.due_date if self.due_date else date.today()
            next_task = Task(
                type_of_task=self.type_of_task,
                priority_level=self.priority_level,
                duration=self.duration,
                time=self.time,
                frequency=self.frequency,
                due_date=base_date + interval,
            )
            self._pet.add_task(next_task)


@dataclass
class Pet:
    name: str
    pet_type: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        """Add a task to this pet and tag it with the pet's name."""
        task.pet_name = self.name
        task._pet = self
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

    def filter_tasks(self, completed: bool = None, pet_name: str = None) -> List[Task]:
        """Return tasks across every pet, optionally filtered by completion
        status and/or pet name.

        Args:
            completed: If not None, keep only tasks with this completion
                status.
            pet_name: If not None, keep only tasks belonging to this pet.

        Returns:
            A new list of Task objects matching every filter that was
            given (an empty list if none match). Passing neither filter
            returns all tasks.

        Algorithm: starts from get_all_tasks() and narrows the list with
        one linear scan (list comprehension) per active filter.
        Time complexity: O(n) per active filter.
        """
        tasks = self.get_all_tasks()
        if completed is not None:
            tasks = [t for t in tasks if t.completed == completed]
        if pet_name is not None:
            tasks = [t for t in tasks if t.pet_name == pet_name]
        return tasks


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

    def sort_by_time(self):
        """Sort the scheduled tasks by their preferred time, earliest first.

        Algorithm: Python's built-in sorted() (Timsort) with a key function
        that reads each task's time string. Tasks with no time set use the
        sentinel "99:99" so they always sort to the end.

        Time complexity: O(n log n), where n is the number of scheduled
        tasks.
        """
        self.scheduled_tasks = sorted(
            self.scheduled_tasks,
            key=lambda t: t.time if t.time else "99:99"
        )

    def find_conflicts(self) -> dict:
        """Detect tasks scheduled at the same time, whether for the same pet
        or different pets.

        Returns:
            A dict mapping each conflicting time string to the list of two
            or more Task objects scheduled at that time (times with only
            one task, or no time set, are left out).

        Algorithm: single-pass grouping/bucketing. Each task's time string
        is used as a dict key, and tasks are appended to a list bucket per
        key; buckets left with only one task are then dropped.
        Time complexity: O(n), where n is the number of scheduled tasks.
        """
        by_time = {}
        for task in self.scheduled_tasks:
            if not task.time:
                continue
            by_time.setdefault(task.time, []).append(task)
        return {time_str: tasks for time_str, tasks in by_time.items() if len(tasks) > 1}

    def get_conflict_warnings(self) -> List[str]:
        """Safely check for scheduling conflicts and describe them as
        human-readable warnings, never raising an exception.

        Returns:
            A list of warning strings, one per conflicting time slot (an
            empty list if there are no conflicts). If the scheduling data
            is missing or malformed, returns a single warning describing
            the problem instead of raising.

        Algorithm: calls find_conflicts() to group tasks by time, then for
        each conflict group builds a set of the involved pet names to
        classify it as "same pet" (set size 1) or "different pets" (set
        size > 1), and formats the details into a warning string. Wrapped
        in try/except so bad input degrades to a warning instead of a
        crash.
        Time complexity: O(n) for grouping, plus O(k) to format the k
        conflict groups found.
        """
        try:
            conflicts = self.find_conflicts()
        except (AttributeError, TypeError) as exc:
            return [f"Warning: could not check for scheduling conflicts ({exc})."]

        warnings = []
        for time_str, tasks in sorted(conflicts.items()):
            pet_names = {t.pet_name for t in tasks}
            scope = "same pet" if len(pet_names) == 1 else "different pets"
            details = ", ".join(f"{t.type_of_task} ({t.pet_name})" for t in tasks)
            warnings.append(f"Warning: scheduling conflict at {time_str} [{scope}]: {details}")
        return warnings

    def display_conflicts(self):
        """Print any scheduling conflicts as warnings, noting whether each
        clash is within the same pet or across different pets."""
        warnings = self.get_conflict_warnings()
        if not warnings:
            print("\nNo scheduling conflicts detected.")
            return
        print("\n=== Scheduling Conflicts ===")
        for warning in warnings:
            print(f"  {warning}")

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

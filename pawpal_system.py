from dataclasses import dataclass
from typing import List


@dataclass
class Pet:
    name: str
    pet_type: str

    def update_pet_info(self, name: str = None, pet_type: str = None):
        pass


@dataclass
class Task:
    type_of_task: str
    priority_level: str
    duration: int

    def add_task(self):
        pass

    def delete_task(self):
        pass

    def edit_task(self, type_of_task: str = None, priority_level: str = None, duration: int = None):
        pass


class DailySchedule:
    def __init__(self, date: str):
        self.date = date
        self.reasoning = ""
        self.tasks: List[Task] = []

    def display_schedule(self):
        pass

    def display_reasoning(self):
        pass


class PetOwner:
    def __init__(self):
        self.name_of_owner = ""
        self.pets: List[Pet] = []
        self.schedule: DailySchedule = None

    def add_name(self, name: str):
        pass

    def add_pet(self, pet: Pet):
        pass

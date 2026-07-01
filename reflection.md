# PawPal+ Project Reflection

## 1. System Design

Actions
- A user should be able to enter information about pet owner and their pet.
- A user should be able to add or edit tasks.
- A user should be able to see the generated daily plan and its reasoning.

Main objects
1. PetOwner
- Attributes: name_of_owner, pets
- Methods: add_name(), add_pet()

2. Pet
- Attributes: name, pet_type
- Methods: update_pet_info()

3. DailySchedule
- Attributes: date, reasoning
- Methods: display_schedule(), display_reasoning()

4. Task
- Attributes: type_of_task, priority_level, duration
- Methods: add_task(), delete_task(), edit_task()

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

I chose 4 classes: PetOwner, Pet, Daily_Schedule and Task. Their responsibilities are:
1. PetOwner: adds their name and their pet(s)
2. Pet: stores the pet's name and type, and also allows updating that info
3. DailySchedule: displays the schedule and its reasoning
4. Task: stores the task details and adding, deleting and editing tasks is possible. 

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes, it did.
Here are some changes I made:
1. Initially, I didn't link a task to a pet. Now, I added a pet_name attritube to the Task class.
2. Although I had a DailySchedule class and had an attribute to display a schedule, I didn't have the attribute that lets the system generate the daily plan/schedule. Now I have the generate_schedule.
3. I had inititally put the add_task and delete_task methods on the Task class, but I had to move it to the PetOwner since they're the ones doing this.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

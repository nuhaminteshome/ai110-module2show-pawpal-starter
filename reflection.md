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

My conflict checker only catches tasks that start at the exact same time (like two tasks both set to "09:00"). It does not check if tasks overlap when their durations are different. For example, a 30-minute walk starting at 07:00 actually runs until 07:30, so it really overlaps with a task starting at 07:15, but my scheduler would not flag that as a conflict since the start times are not identical.

I think this is a reasonable tradeoff for now because comparing exact times is much simpler to write and understand than comparing time ranges (which would need converting times to actual start/end minutes and checking if those ranges cross each other). 

---

## 3. AI Collaboration

**a. How you used AI**

- I used AI as a tool to ask questions, review my code and explain parts of the code when I didn't understand the logic. It also helped me with coming up with different edge cases.

**b. Judgment and verification**

One moment I didn't just accept what the AI did was when it tried to start my Streamlit app for me by running a command in the background. I said no, because I wanted to run it myself in my own terminal. When I ran it myself, I got a "No module named streamlit" error. The AI helped me figure out that I had the wrong virtual environment activated (the outer project venv instead of the one inside my pawpal folder that actually has streamlit installed), but I verified this myself by checking the folder paths and picking the correct venv to activate.

---

## 4. Testing and Verification

**a. What you tested**

I tested:

1. whether my scheduler sorts tasks correctly
2. whether marking a recurring task complete creates the next occurrence with the correct due date
3. whether my conflict checker correctly flags tasks at the same time.


**b. Confidence**

I feel fairly confident my scheduler works correctly for the cases I tested, since I have 24 passing tests covering sorting, recurrence, and conflicts. If I had more time, I would test overlapping tasks with different durations.

---

## 5. Reflection

**a. What went well**

- I was happy with how the conflict detection worked.


**b. What you would improve**

I would make the conflict checker smarter, so it catches tasks that overlap in time, not just ones that start at the exact same minute.

**c. Key takeaway**

I learned how system design works and its implementation.


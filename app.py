from pawpal_system import Task, Pet, PetOwner, DailySchedule
import streamlit as st

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

# --- Initialize session state ---
if "owner" not in st.session_state:
    st.session_state.owner = PetOwner()

if "pet" not in st.session_state:
    st.session_state.pet = None

# --- Owner & Pet Info ---
st.subheader("Owner & Pet Info")

owner_name = st.text_input("Owner name", value="Jordan")
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Save Owner & Pet"):
    st.session_state.owner.add_name(owner_name)       # PetOwner.add_name()
    pet = Pet(name=pet_name, pet_type=species)
    st.session_state.owner.pets = [pet]               # reset to one pet for now
    st.session_state.pet = pet
    st.session_state.owner.add_pet                    # PetOwner.add_pet() wired above
    st.success(f"Saved {owner_name} with pet {pet_name} the {species}.")

if st.session_state.owner.pets:
    st.write("Current pets:")
    for p in st.session_state.owner.pets:
        st.write(f"- {p.name} ({p.pet_type})")

st.divider()

# --- Add Tasks ---
st.subheader("Tasks")
st.caption("Tasks are added to your pet and fed into the scheduler.")

col1, col2, col3, col4 = st.columns(4)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
with col4:
    time = st.text_input("Time (HH:MM)", value="08:00")

if st.button("Add Task"):
    if st.session_state.pet is None:
        st.warning("Save an owner and pet first.")
    else:
        task = Task(
            type_of_task=task_title,
            priority_level=priority,
            duration=int(duration),
            time=time
        )
        st.session_state.pet.add_task(task)           # Pet.add_task()
        st.success(f"Added '{task_title}' to {st.session_state.pet.name}.")

if st.session_state.pet and st.session_state.pet.tasks:
    status_filter = st.radio(
        "Show", ["All", "Pending", "Completed"], horizontal=True
    )
    if status_filter == "Pending":
        visible_tasks = st.session_state.owner.filter_tasks(
            completed=False, pet_name=st.session_state.pet.name
        )
    elif status_filter == "Completed":
        visible_tasks = st.session_state.owner.filter_tasks(
            completed=True, pet_name=st.session_state.pet.name
        )
    else:
        visible_tasks = st.session_state.owner.filter_tasks(
            pet_name=st.session_state.pet.name
        )                                               # PetOwner.filter_tasks()

    if visible_tasks:
        st.table([
            {
                "Task": t.type_of_task,
                "Pet": t.pet_name,
                "Time": t.time,
                "Duration (min)": t.duration,
                "Priority": t.priority_level,
                "Status": "✅ done" if t.completed else "⏳ pending",
            }
            for t in visible_tasks
        ])
    else:
        st.info(f"No {status_filter.lower()} tasks.")
else:
    st.info("No tasks yet. Add one above.")

st.divider()

# --- Generate Schedule ---
st.subheader("Build Schedule")

sort_by_time = st.checkbox("Sort by time instead of priority")

if st.button("Generate Schedule"):
    owner = st.session_state.owner
    if not owner.get_all_tasks():
        st.warning("Add at least one task before generating a schedule.")
    else:
        schedule = DailySchedule(date="2026-07-01", owner=owner)
        schedule.generate_schedule()                  # DailySchedule.generate_schedule()
        if sort_by_time:
            schedule.sort_by_time()                    # DailySchedule.sort_by_time()

        st.success("Schedule generated!")

        # --- Conflicts surfaced first so the owner sees them before the plan ---
        conflicts = schedule.find_conflicts()          # DailySchedule.find_conflicts()
        if conflicts:
            st.markdown("#### ⚠️ Conflicts")
            for time_str, tasks in sorted(conflicts.items()):
                pet_names = {t.pet_name for t in tasks}
                details = ", ".join(f"{t.type_of_task} ({t.pet_name})" for t in tasks)
                if len(pet_names) == 1:
                    # Same pet double-booked: literally impossible to do both.
                    st.error(f"**{time_str}** — {details} can't happen at once for {tasks[0].pet_name}.")
                else:
                    # Different pets, same time: tight but possibly workable for the owner.
                    st.warning(f"**{time_str}** — {details} are scheduled at the same time.")
        else:
            st.success("No scheduling conflicts detected.")

        st.markdown("#### Today's Schedule")
        st.table([
            {
                "Time": task.time if task.time else "??:??",
                "Task": task.type_of_task,
                "Pet": task.pet_name,
                "Duration (min)": task.duration,
                "Priority": task.priority_level,
                "Status": "✅ done" if task.completed else "⏳ pending",
            }
            for task in schedule.scheduled_tasks
        ])

        st.markdown("#### Reasoning")
        st.info(schedule.reasoning)

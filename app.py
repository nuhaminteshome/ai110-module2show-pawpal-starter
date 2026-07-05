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
    st.write("Current tasks:")
    st.table([
        {
            "Task": t.type_of_task,
            "Pet": t.pet_name,
            "Time": t.time,
            "Duration (min)": t.duration,
            "Priority": t.priority_level,
            "Done": t.completed,
        }
        for t in st.session_state.pet.tasks
    ])
else:
    st.info("No tasks yet. Add one above.")

st.divider()

# --- Generate Schedule ---
st.subheader("Build Schedule")

if st.button("Generate Schedule"):
    owner = st.session_state.owner
    if not owner.get_all_tasks():
        st.warning("Add at least one task before generating a schedule.")
    else:
        schedule = DailySchedule(date="2026-07-01", owner=owner)
        schedule.generate_schedule()                  # DailySchedule.generate_schedule()

        st.success("Schedule generated!")

        st.markdown("#### Today's Schedule")
        for task in schedule.scheduled_tasks:
            st.markdown(
                f"- **{task.time}** — {task.type_of_task} ({task.pet_name}) "
                f"| {task.duration} min | Priority: `{task.priority_level}`"
            )

        st.markdown("#### Reasoning")
        st.info(schedule.reasoning)

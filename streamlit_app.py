import streamlit as st
from app.core.notifier import send_email
from app.core.database import init_db
from app.modules.subscriptions.service import subscribe
from app.modules.exams.timetable_service import (
    load_timetable,
    list_available_programs_from_ical
)
from app.data.programs import PROGRAM_NAME_MAP

# -------------------------------
# Helpers
# -------------------------------
def get_first_name_from_email(email: str) -> str:
    local_part = email.split("@")[0]
    return local_part.split(".")[0].capitalize()

# -------------------------------
# Initialization
# -------------------------------
init_db()
st.title("Student Exam Reminder")

if "exams" not in st.session_state:
    st.session_state.exams = None

# -------------------------------
# Step 1: Program / Year / Semester
# -------------------------------
st.header("Select Your Program and Semester")

programs = list_available_programs_from_ical()

if not programs:
    st.error("No programs available.")
    st.stop()

program_code = st.selectbox(
    "Program",
    options=list(programs.keys()),
    format_func=lambda code: programs[code]
)

year = st.selectbox("Year of Study", [1, 2, 3])
semester = st.selectbox("Semester", [1, 2])

# -------------------------------
# Step 2: Load Courses
# -------------------------------
if st.button("Load Courses"):
    try:
        st.session_state.exams = load_timetable(program_code, year, semester)
    except Exception as e:
        st.error(str(e))

# -------------------------------
# Step 3: Subscribe
# -------------------------------
if st.session_state.exams:
    course_names = sorted(
        {exam["course"] for exam in st.session_state.exams}
    )

    st.subheader("Available Courses")

    selected_courses = st.multiselect(
        "Select courses to receive reminders for",
        course_names
    )

    manual_course = st.text_input(
        "Or enter a course manually (must exist above)"
    )

    email = st.text_input("Email address")

    if st.button("Subscribe"):
        final_courses = selected_courses.copy()

        if manual_course:
            if manual_course not in course_names:
                st.error("Entered course does not exist.")
                st.stop()
            final_courses.append(manual_course)

        if not email:
            st.error("Please enter an email address.")
            st.stop()

        if not final_courses:
            st.error("Please select at least one course.")
            st.stop()

        first_name = get_first_name_from_email(email)

        for course in final_courses:
            subscribe(course, email)
            send_email(
                email,
                f"Subscription confirmed – {course}",
                f"""Hej {first_name}!

You have now subscribed to exam reminders.

Course: {course}

You will receive notifications when:
- Exam registration opens
- Mid registration reminder
- 3 days before registration closes

Good luck with your studies!
"""
            )

        st.success("✅ Subscription successful!")

# -------------------------------
# Reset
# -------------------------------
st.divider()
if st.button("Reset Selection"):
    st.session_state.exams = None
    st.rerun()

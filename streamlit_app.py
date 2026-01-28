import streamlit as st
from app.core.notifier import send_email
from app.core.database import init_db
from app.modules.subscriptions.service import subscribe
from app.modules.exams.timetable_service import (
    load_timetable,
    list_available_programs_from_ical
)

# -------------------------------
# Initialization
# -------------------------------
init_db()

def get_first_name_from_email(email: str) -> str:
    local_part = email.split("@")[0]
    first_name = local_part.split(".")[0]
    return first_name.capitalize()


st.title("Student Exam Reminder")

# Session state initialization
if "exams" not in st.session_state:
    st.session_state.exams = None

if "program" not in st.session_state:
    st.session_state.program = None

# -------------------------------
# Step 1: Program / Year / Semester
# -------------------------------
st.header("Select Your Program and Semester")

programs = list_available_programs_from_ical()

if not programs:
    st.error("No programs available. Please contact the administrator.")
    st.stop()

program = st.selectbox("Program", programs)
year = st.selectbox("Year of Study", [1, 2, 3])
semester = st.selectbox("Semester", [1, 2])

# -------------------------------
# Step 2: Load Courses
# -------------------------------
if st.button("Load Courses"):
    try:
        st.session_state.exams = load_timetable(program, year, semester)
        st.session_state.program = program
    except Exception as e:
        st.error(str(e))

# -------------------------------
# Step 3: Course Selection + Subscribe
# -------------------------------
if st.session_state.exams:
    st.subheader("Available Courses")

    course_names = sorted(
        {exam["course"] for exam in st.session_state.exams}
    )

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

        # Validate manual course
        if manual_course:
            if manual_course not in course_names:
                st.error("Entered course does not exist in this program.")
                st.stop()
            final_courses.append(manual_course)

        # Validate email
        if not email:
            st.error("Please enter an email address.")
            st.stop()

        # Validate course selection
        if not final_courses:
            st.error("Please select at least one course.")
            st.stop()

        # Subscribe and notify
        for course in final_courses:
            first_name = get_first_name_from_email(email)
            try:
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
            except Exception as e:
                st.error(f"Failed to subscribe for {course}: {e}")

        st.success("✅ Subscription successful!")

# -------------------------------
# Optional reset
# -------------------------------
st.divider()
if st.button("Reset Selection"):
    st.session_state.exams = None
    st.session_state.program = None
    st.rerun()

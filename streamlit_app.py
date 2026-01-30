import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

import streamlit as st


import streamlit as st
from app.core.database import init_db
from app.core.notifier import send_confirmation_email, generate_token
from app.modules.subscriptions.service import subscribe
from app.modules.exams.timetable_service import (
    load_timetable,
    list_available_programs_from_ical
)
from app.core.unsubscribe import unsubscribe


# -------------------------------
# Initialization
# -------------------------------
init_db()
st.title("🎓 Student Exam Reminder")

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

# year = st.selectbox("Year of Study", [1, 2, 3])
# semester = st.selectbox("Semester", [1, 2])
semester = st.radio(
    "Semester",
    options=[1, 2],
    horizontal=True
)


# -------------------------------
# Step 2: Load Courses
# -------------------------------
if st.button("Load Courses"):
    try:
        #st.session_state.exams = load_timetable(program_code, year, semester)
        st.session_state.exams = load_timetable(program_code, semester)

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
    exam_date_map = {
    exam["course"]: exam["exam_date"]
    for exam in st.session_state.exams
}


    manual_course = st.text_input(
        "Or enter a course manually (must exist above)"
    )

    email = st.text_input("Email address")

    language = st.selectbox(
        "Language / Språk",
        options=["en", "sv"],
        format_func=lambda x: "English" if x == "en" else "Svenska"
    )

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

        unsubscribe_token = generate_token()

        for course in final_courses:
            subscribe(
                course_code=course,
                email=email,
                language=language,
                unsubscribe_token=unsubscribe_token
            )

        BASE_URL = "http://localhost:8501"  # change later when deployed

        course_dates = {
            course: exam_date_map[course]
            for course in final_courses
        }

        send_confirmation_email(
            email=email,
            language=language,
            courses=course_dates,
            unsubscribe_token=unsubscribe_token,
            base_url=BASE_URL
        )


        st.success("✅ Subscription successful!")

# -------------------------------
# Reset
# -------------------------------
st.divider()
if st.button("Reset Selection"):
    st.session_state.exams = None
    st.rerun()

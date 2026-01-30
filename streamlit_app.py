import sys
from pathlib import Path

# -------------------------------
# Ensure project root is on path
# -------------------------------
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

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
# Handle unsubscribe via URL
# -------------------------------
params = st.query_params
if "unsubscribe" in params:
    token = params["unsubscribe"]
    unsubscribe(token)
    st.success("✅ You have been unsubscribed from exam reminders.")
    st.stop()

# -------------------------------
# Initialization
# -------------------------------
init_db()
st.title("🎓 Student Exam Reminder")

if "exams" not in st.session_state:
    st.session_state.exams = None

# -------------------------------
# Step 1: Program + Semester
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
        st.session_state.exams = load_timetable(program_code, semester)
    except Exception as e:
        st.error(str(e))

# -------------------------------
# Step 3: Subscribe
# -------------------------------
if st.session_state.exams:
    # Build course list
    course_names = sorted({exam["course"] for exam in st.session_state.exams})

    # Map course → exam_date (authoritative source)
    exam_date_map = {
        exam["course"]: exam["exam_date"]
        for exam in st.session_state.exams
        if "exam_date" in exam
    }

    st.subheader("Available Courses")

    selected_courses = st.multiselect(
        "Select courses to receive reminders for",
        course_names
    )

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

        # One token per user (shared across courses)
        tokens = []

        for course in final_courses:
            token = subscribe(
            course_code=course,
            email=email,
            language=language
            )
            tokens.append(token)

        # use first token for email unsubscribe link
        unsubscribe_token = tokens[0]

        # Build course → date mapping for email
        course_dates = {
            course: exam_date_map.get(course)
            for course in final_courses
        }

        BASE_URL = st.get_option("server.baseUrlPath") or "http://localhost:8501"

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

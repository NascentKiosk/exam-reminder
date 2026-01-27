import streamlit as st
from app.core.notifier import send_email
from app.core.database import init_db
from app.modules.subscriptions.service import subscribe
from app.modules.exams.timetable_service import load_timetable, list_available_programs_from_ical

# Initialize database
init_db()

st.title("Student Exam Reminder")

# --- Step 1: Select program from dropdown ---
st.header("Select Your Program and Semester")

available_programs = list_available_programs_from_ical()

if not available_programs:
    st.error("No programs found in the backend. Please check timetables folder.")
else:
    program = st.selectbox("Program", available_programs)
    year = st.number_input("Year", min_value=1, max_value=6, step=1)
    semester = st.number_input("Semester", min_value=1, max_value=2, step=1)

# Button to load courses
if st.button("Load Courses"):
    try:
        # --- Load courses from backend iCal files ---
        exams = load_timetable(program, year, semester)
        course_names = [exam["course"] for exam in exams]

        if not course_names:
            st.warning("No courses found for this selection.")
        else:
            # --- Step 2: Student selects courses ---
            selected_courses = st.multiselect(
                "Select courses to get reminders for",
                course_names
            )

            # --- Step 3: Optional manual course entry ---
            manual_course = st.text_input(
                "Or enter a course manually (must exist in timetable)"
            )

            email = st.text_input("Email for reminders")

            if st.button("Subscribe to Selected Courses"):
                final_courses = selected_courses.copy()

                # Validate manual course
                if manual_course:
                    if manual_course not in course_names:
                        st.error(f"Course '{manual_course}' not found in timetable.")
                    else:
                        final_courses.append(manual_course)

                # Check if email and courses are provided
                if not email:
                    st.error("Please enter your email.")
                elif not final_courses:
                    st.error("Please select or enter at least one course.")
                else:
                    # Subscribe and send confirmation emails
                    for course in final_courses:
                        try:
                            subscribe(course, email)
                            send_email(
                                email,
                                f"Subscription confirmed – {course}",
                                f"You are subscribed to reminders for {course}."
                            )
                        except Exception as e:
                            st.error(f"Failed to subscribe for {course}: {e}")

                    if final_courses:
                        st.success("Subscribed successfully for selected courses!")

    except FileNotFoundError as e:
        st.error(str(e))
    except Exception as e:
        st.error(f"Unexpected error: {e}")

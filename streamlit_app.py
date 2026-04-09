import os
import logging
import streamlit as st

from opencensus.ext.azure.log_exporter import AzureLogHandler
from app.core.notifier import send_email
from app.core.database import init_db
from app.modules.subscriptions.service import subscribe


# ================================
# LOGGING SETUP (Azure Insights)
# ================================
logger = logging.getLogger("exam-reminder")
logger.setLevel(logging.INFO)

connection_string = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")

if connection_string and not logger.handlers:
    handler = AzureLogHandler(connection_string=connection_string)
    logger.addHandler(handler)

# 👇 FORCE execution inside Streamlit run
st.write("")  # forces script execution
logger.error("🚨 TEST LOG FROM STREAMLIT")


# ================================
# INITIALIZE DATABASE
# ================================
init_db()


# ================================
# STREAMLIT UI
# ================================
st.title("Student Exam Reminder v6")

course = st.text_input("Course Code")
email = st.text_input("Email")


if st.button("Subscribe"):
    if course and email:
        try:
            # Save subscription
            subscribe(course, email)

            # Log success
            logger.info(f"User subscribed: {email} -> {course}")

            # Send confirmation email
            send_email(
                email,
                f"Subscription confirmed – {course.upper()}",
                f"""
You are now subscribed to exam reminders.

Course: {course.upper()}

You will receive notifications when:
- Exam registration opens
- Mid registration reminder
- 3 days before registration closes

Good luck with your studies!
"""
            )

            st.success("Subscribed successfully! Confirmation email sent.")

        except ValueError as e:
            logger.warning(f"Validation error: {str(e)}")
            st.warning(str(e))

        except Exception as e:
            logger.error(f"Subscription failed: {str(e)}")
            st.error("Failed to send confirmation email.")

    else:
        logger.warning("User submitted empty form")
        st.error("Please enter both course code and email.")
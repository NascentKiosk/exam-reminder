import os
import logging
import streamlit as st

from opencensus.ext.azure.log_exporter import AzureLogHandler
from app.core.notifier import send_email
from app.core.database import init_db
from app.modules.subscriptions.service import subscribe


# ================================
# DEBUG (VISIBLE IN CONTAINER LOGS)
# ================================
print("APP STARTED - STDOUT WORKS")




# ================================
# LOGGING SETUP (APPLICATION INSIGHTS)
# ================================
logger = logging.getLogger("exam-reminder")
logger.setLevel(logging.INFO)

connection_string = os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")

if connection_string and not logger.handlers:
    handler = AzureLogHandler(connection_string=connection_string)
    logger.addHandler(handler)

# Send test logs to Application Insights
logger.info("APP STARTED - LOGGING WORKS")
logger.error("TEST ERROR LOG")



# ================================
# INITIALIZE DATABASE
# ================================
init_db()


# ================================
# STREAMLIT UI
# ================================
st.title("Student Exam Reminder v7")

course = st.text_input("Course Code")
email = st.text_input("Email")


if st.button("Subscribe"):
    if course and email:
        try:
            # Save subscription
            subscribe(course, email)

            print(f"✅ SUBSCRIPTION (stdout): {email} -> {course}")
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
            print(f"⚠️ VALIDATION ERROR: {str(e)}")
            logger.warning(f"Validation error: {str(e)}")
            st.warning(str(e))

        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
            logger.error(f"Subscription failed: {str(e)}")
            st.error("Failed to send confirmation email.")

    else:
        print("⚠️ EMPTY INPUT")
        logger.warning("User submitted empty form")
        st.error("Please enter both course code and email.")
        
raise Exception("Test alert")
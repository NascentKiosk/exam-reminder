

import os
import logging
import streamlit as st


from opencensus.ext.azure.log_exporter import AzureLogHandler
from app.core.notifier import send_email
from app.core.database import init_db
from app.modules.subscriptions.service import subscribe

print("APP STARTED - NEW VERSION")

logger = logging.getLogger(__name__)

if os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING"):
    logger.addHandler(
        AzureLogHandler(
            connection_string=os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING")
        )
    )

logger.setLevel(logging.INFO)
logger.info(" Streamlit app starting...")

# 👇 VERY IMPORTANT
init_db()


st.title("Student Exam Reminder v9")


course = st.text_input("Course Code")
email = st.text_input("Email")

if st.button("Subscribe"):
    if course and email:
        try:
            subscribe(course, email)

            # ✅ Confirmation email
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
            st.warning(str(e))
        except Exception as e:
            st.error("Failed to send confirmation email.")
        #except Exception as e:
            #st.error(f"Email error: {e}")
    else:
        st.error("Please enter both course code and email.")





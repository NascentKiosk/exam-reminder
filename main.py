import logging
import os
from opencensus.ext.azure.log_exporter import AzureLogHandler

from app.core.database import init_db
#from app.core.scheduler import show_countdowns
#from app.core.notifier import send_email, send_sms
from app.modules.exams.service import add_exam

# ----------------------------
# Initialize logging
# ----------------------------
logger = logging.getLogger(__name__)

# Use environment variable from manual connection string method
connection_str = os.environ.get("APPLICATIONINSIGHTS_CONNECTION_STRING")

if connection_str:
    logger.addHandler(AzureLogHandler(connection_string=connection_str))

logger.setLevel(logging.INFO)

# ----------------------------
# Menu functions
# ----------------------------
def menu():
    print("\n===== Exam Reminder System =====")
    print("1. Add a new exam")
    print("2. View exams & countdowns")
    print("3. Send email reminders")
    # print("4. Send SMS reminders") # Temporarily disabled
    print("5. Exit")

def handle_add_exam():
    try:
        course = input("Course name: ")
        exam_date = input("Exam date (YYYY-MM-DD): ")
        notes = input("Notes (optional): ")

        add_exam(course, exam_date, notes)
        print("✅ Exam added successfully")
        logger.info(f"Exam added: {course} on {exam_date}")

    except ValueError:
        print("❌ Invalid date format. Use YYYY-MM-DD.")
        logger.warning("User entered invalid date format")
    except Exception as e:
        print("❌ Failed to add exam:", e)
        logger.error(f"Error adding exam: {str(e)}")

def handle_email():
    try:
        to_email = input("Send email to: ")
        subject = "Exam Reminder"
        body = "Check your exam signup and deadlines."
        send_email(subject, body, to_email)
        print("📧 Email sent")
        logger.info(f"Email sent to: {to_email}")
    except Exception as e:
        print("❌ Failed to send email:", e)
        logger.error(f"Error sending email: {str(e)}")

def handle_sms():
    try:
        number = input("Phone number (+countrycode): ")
        message = "Exam reminder: check signup deadlines."
        send_sms(number, message)
        print("📱 SMS sent")
        logger.info(f"SMS sent to: {number}")
    except Exception as e:
        print("❌ Failed to send SMS:", e)
        logger.error(f"Error sending SMS: {str(e)}")

# ----------------------------
# Main loop
# ----------------------------
def main():
    logger.info("App started")
    init_db()

    while True:
        menu()
        choice = input("Choose an option: ")

        if choice == "1":
            handle_add_exam()
        elif choice == "2":
            show_countdowns()
        elif choice == "3":
            handle_email()
        elif choice == "4":
            # handle_sms()  # Disabled for now
            print("SMS feature temporarily disabled.")
        elif choice == "5":
            print("Goodbye 👋")
            logger.info("App exited by user")
            break
        else:
            print("❌ Invalid choice")
            logger.warning(f"Invalid menu choice: {choice}")

if __name__ == "__main__":
    main()
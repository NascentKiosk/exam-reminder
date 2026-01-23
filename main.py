from app.core.database import init_db
from app.core.scheduler import show_countdowns
from app.core.notifier import send_email, send_sms
from app.modules.exams.service import add_exam

def menu():
    print("\n===== Exam Reminder System =====")
    print("1. Add a new exam")
    print("2. View exams & countdowns")
    print("3. Send email reminders")
    print("4. Send SMS reminders")
    print("5. Exit")

def handle_add_exam():
    course = input("Course name: ")
    exam_date = input("Exam date (YYYY-MM-DD): ")
    signup_start = input("Signup start date (YYYY-MM-DD): ")
    signup_end = input("Signup end date (YYYY-MM-DD): ")
    notes = input("Notes (optional): ")

    add_exam(course, exam_date, signup_start, signup_end, notes)
    print("✅ Exam added successfully")

def handle_email():
    to_email = input("Send email to: ")
    subject = "Exam Reminder"
    body = "Check your exam signup and deadlines."
    send_email(subject, body, to_email)
    print("📧 Email sent")

def handle_sms():
    number = input("Phone number (+countrycode): ")
    message = "Exam reminder: check signup deadlines."
    send_sms(number, message)
    print("📱 SMS sent")

def main():
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
            handle_sms()
        elif choice == "5":
            print("Goodbye 👋")
            break
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    main()

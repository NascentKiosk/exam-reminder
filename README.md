# 📚 Exam Reminder System

A Python-based automated reminder system that helps university students **never miss exam registration deadlines**.

The system fetches exam data, stores subscriptions, and sends **email reminders automatically**, even when the app, VS Code, or Streamlit is closed.

---

## 🚀 Features

* 📅 Tracks exam dates per course
* ⏰ Automatically calculates registration windows

  * Registration opens **50 days before exam**
  * Registration closes **14 days before exam**
* 📧 Sends email reminders:

  * When registration opens
  * Midway reminder
  * 3 days before registration closes
* 🖥 Runs daily in the background using **Windows Task Scheduler**
* 💾 Uses **SQLite** for persistence
* 🔌 Decoupled from Streamlit (backend keeps working even if UI is closed)

---

## 🧠 Architecture Overview

```
Streamlit UI
   ↓
SQLite Database (exams.db)
   ↓
Windows Task Scheduler (daily)
   ↓
reminder_engine.py → Email notifications
```

---

## 🗂 Project Structure

```
exam-reminder/
│
├── app/
│   ├── core/
│   │   ├── database.py          # DB connection & schema
│   │   ├── notifier.py          # Email sending logic
│   │   └── reminder_engine.py   # Reminder scheduling logic
│   │
│   └── modules/                 # Timetable & subscription logic
│
├── data/
│   └── exams.db                 # SQLite database (auto-created)
│
├── run_reminders.py             # Entry point for scheduler
├── streamlit_app.py             # UI for student subscriptions
├── .env                         # Email credentials (not committed)
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the repository

```bash
git clone https://github.com/NascentKiosk/exam-reminder.git
cd exam-reminder
```

---

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Configure email credentials

Create a `.env` file in the project root:

```
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
```

> ⚠️ Use a Gmail **App Password**, not your real password.

---

### 4️⃣ Run the Streamlit app (optional UI)

```bash
streamlit run streamlit_app.py
```

Use this to:

* Select program & courses
* Subscribe email addresses

---

## 🔁 Automated Reminders (Background Service)

The reminder system runs **independently** of Streamlit using **Windows Task Scheduler**.

### Reminder logic lives in:

```
app/core/reminder_engine.py
```

Each day it:

1. Loads subscriptions
2. Checks exam dates
3. Determines if a reminder is due
4. Sends email (once per stage)

---

## 🪟 Windows Task Scheduler Setup (Summary)

* Task name: `Exam Reminder Service`
* Runs: **Daily (e.g. 09:00)**
* Program:

  ```
  python.exe
  ```
* Arguments:

  ```
  run_reminders.py
  ```
* Start in:

  ```
  exam-reminder/
  ```
* Run whether user is logged on or not
* Run with highest privileges

---

## 🧪 Testing

### Dry-run (no emails sent)

```bash
python -c "from app.core.reminder_engine import run_reminders; run_reminders(dry_run=True)"
```

### Manual run

```bash
python run_reminders.py
```

---

## 🔐 Security Notes

* `.env` is ignored via `.gitignore`
* No passwords are stored in code
* SQLite is local-only

---

## 📌 Future Improvements

* Logging to file
* Admin dashboard (Streamlit)
* SMS / push notifications
* Docker support
* Multi-university support

---

## 👨‍🎓 Author

Built by a software engineering student to solve a **real university problem**.

---

## 📜 License

MIT License

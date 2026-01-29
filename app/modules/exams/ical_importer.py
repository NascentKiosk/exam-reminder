from datetime import datetime
from app.modules.exams.service import add_exam
from app.modules.exams.ical_reader import read_ical  # from Step 2

def import_ical(file_path):
    """
    Read an iCal file and add exams to the database.
    """
    exams = read_ical(file_path)

    for exam in exams:
        add_exam(
            exam["course"],
            exam["date"].isoformat(),
            "Imported from iCal"
        )

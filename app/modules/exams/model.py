from dataclasses import dataclass

@dataclass
class Exam:
    course_name: str
    exam_date: str
    signup_start: str
    signup_end: str
    notes: str = ""

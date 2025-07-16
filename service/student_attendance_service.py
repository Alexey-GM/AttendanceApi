from sqlalchemy.orm import Session
from datetime import date, timedelta
from data.models.attendance import Attendance
from data.models.schedule import Schedule
from data.models.subject import Subject
from data.models.student import Student

def get_all_students(db: Session):
    students = db.query(Student).all()
    return [{
        "id": s.id,
        "full_name": f"{s.last_name} {s.first_name[0]}.{s.middle_name[0] if s.middle_name else ''}."
    } for s in students]

def get_subjects_for_student(db: Session, student_id: int):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        return []

    group_id = student.group_id

    subject_ids = db.query(Schedule.student_subject).filter(
        Schedule.group_id == group_id
    ).distinct().all()

    subject_ids = [s[0] for s in subject_ids] 

    if not subject_ids:
        return []

    subjects = db.query(Subject).filter(Subject.id.in_(subject_ids)).all()

    return [{"id": s.id, "name": s.name} for s in subjects]

##def get_last_4_weeks():
##  today = date.today()
##  weeks = []
##  for i in range(4):
##    monday = today - timedelta(days=today.weekday() + i * 7)
##    sunday = monday + timedelta(days=6)
##    weeks.append((monday, sunday))
##  return list(reversed(weeks))

def get_last_4_weeks():
    return [
        (date(2024, 10, 7), date(2024, 10, 13)),
        (date(2024, 10, 14), date(2024, 10, 20)),
        (date(2024, 10, 21), date(2024, 10, 27)),
        (date(2024, 10, 28), date(2024, 11, 3)),
    ]

def get_student_weekly_attendance(db: Session, student_id: int, subject_id: int, type_class: str):
    weeks = get_last_4_weeks()
    response = []

    for start_date, end_date in weeks:
        schedules = db.query(Schedule).filter(
            Schedule.student_subject == subject_id,
            Schedule.type_class == type_class,
            Schedule.date >= start_date,
            Schedule.date <= end_date
        ).all()

        schedule_ids = [s.id for s in schedules]
        if not schedule_ids:
            response.append(0)
            continue

        attendances = db.query(Attendance).filter(
            Attendance.schedule.in_(schedule_ids),
            Attendance.student == student_id
        ).all()

        total = len(attendances)
        present = len([a for a in attendances if a.status == 1])

        percent = round((present / total) * 100) if total > 0 else 0
        response.append(percent)

    return response

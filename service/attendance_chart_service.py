from sqlalchemy.orm import Session
from data.models.attendance import Attendance
from data.models.schedule import Schedule
from data.models.student import Student
from data.models.student_group import StudentGroup
from datetime import date, timedelta
from collections import defaultdict

def get_attendance_summary(db: Session, period: str):
    today = date.today()
    
    if period == "Прошлая неделя":
        start_date = today - timedelta(days=7)
    elif period == "Прошлый месяц":
        start_date = today - timedelta(days=30)
    elif period == "Прошлый семестр":
        year = today.year if today.month > 6 else today.year - 1
        if today.month >= 9:
            start_date = date(year, 9, 1)
            end_date = date(year + 1, 1, 31)
        else:
            start_date = date(year, 2, 1)
            end_date = date(year, 6, 30)
    else:
        return []

    query = db.query(
        StudentGroup.course,
        Attendance.status
    ).join(
        Schedule, Attendance.schedule == Schedule.id
    ).join(
        Student, Attendance.student == Student.id
    ).join(
        StudentGroup, Student.group_id == StudentGroup.id
    )

    if period == "Прошлый семестр":
        query = query.filter(Schedule.date >= start_date, Schedule.date <= end_date)
    else:
        query = query.filter(Schedule.date >= start_date)

    results = query.all()

    summary = defaultdict(lambda: {'present': 0, 'total': 0})

    for course, status in results:
        summary[course]['total'] += 1
        if status == 1: 
            summary[course]['present'] += 1

    response = []
    for course in sorted(summary.keys()):
        s = summary[course]
        attendance = round((s['present'] / s['total']) * 100) if s['total'] else 0
        response.append({
            "course": f"{course} курс",
            "attendance": attendance
        })

    return response

from datetime import date
from sqlalchemy.orm import Session
from data.models.attendance import Attendance
from data.models.schedule import Schedule
from data.models.student import Student
from data.models.student_group import StudentGroup

def get_group_attendance(
    db: Session,
    start_date: date,
    end_date: date,
    course: int = None,
    direction: str = None
):
    query = (
        db.query(
            StudentGroup.name.label("group"),
            Schedule.date,
            Attendance.status
        )
        .join(Schedule, Schedule.group_id == StudentGroup.id)
        .join(Attendance, Attendance.schedule == Schedule.id)
        .filter(Schedule.date >= start_date, Schedule.date <= end_date)
    )

    if course:
        query = query.filter(StudentGroup.course == course)
    if direction:
        query = query.filter(StudentGroup.direction == direction)

    rows = query.all()

    result = {}
    for group, sched_date, status in rows:
        if group not in result:
            result[group] = {}
        date_str = sched_date.strftime("%d.%m")
        if date_str not in result[group]:
            result[group][date_str] = {"present": 0, "total": 0}

        result[group][date_str]["total"] += 1
        if status == 1: 
            result[group][date_str]["present"] += 1

    all_dates = sorted({d for group_data in result.values() for d in group_data})
    final_data = []
    for date_str in all_dates:
        day_data = {"date": date_str}
        for group, group_data in result.items():
            if date_str in group_data:
                attendance = group_data[date_str]
                percent = round(attendance["present"] / attendance["total"] * 100, 2)
                day_data[group] = percent
            else:
                day_data[group] = 0
        final_data.append(day_data)

    return final_data

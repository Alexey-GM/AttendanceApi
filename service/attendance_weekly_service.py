from sqlalchemy.orm import Session
from data.models.attendance import Attendance
from data.models.schedule import Schedule
from data.models.student import Student
from data.models.student_group import StudentGroup
from datetime import date, timedelta
from collections import defaultdict
import calendar

##def get_last_4_weeks():
##  today = date.today()
##  weeks = []
##  for i in range(4):
##      monday = today - timedelta(days=today.weekday() + i * 7)
##      sunday = monday + timedelta(days=6)
##      weeks.append((monday, sunday))
##  return list(reversed(weeks))

def get_last_4_weeks():
    return [
        (date(2025, 2, 3), date(2025, 2, 9)),
        (date(2025, 2, 10), date(2025, 2, 16)),
        (date(2025, 2, 17), date(2025, 2, 23)),
        (date(2025, 2, 24), date(2025, 3, 2)),
    ]

def get_weekly_attendance(db: Session, direction: str = None, course: int = None):
    weeks = get_last_4_weeks()
    response = []

    for start_date, end_date in weeks:
        week_num = start_date.isocalendar()[1]
        even = week_num % 2 == 0
        formatted_range = f"{start_date.strftime('%d.%m')} - {end_date.strftime('%d.%m')}"
        week_label = f"{'Чет' if even else 'Нечет'} / {formatted_range}"

        groups_query = db.query(StudentGroup)
        if direction:
            groups_query = groups_query.filter(StudentGroup.direction == direction)
        if course:
            groups_query = groups_query.filter(StudentGroup.course == course)

        groups = groups_query.all()

        week_data = []
        for group in groups:
            schedules = db.query(Schedule).filter(
                Schedule.group_id == group.id,
                Schedule.date >= start_date,
                Schedule.date <= end_date
            ).all()

            schedule_ids = [s.id for s in schedules]
            if not schedule_ids:
                continue

            attendances = db.query(Attendance).filter(
                Attendance.schedule.in_(schedule_ids)
            ).all()

            total = len(attendances)
            present = len([a for a in attendances if a.status == 1])

            percent = round((present / total) * 100) if total > 0 else 0

            week_data.append({
                "group": group.name,
                "direction": group.direction,
                "value": percent
            })

        response.append({
            "week": week_label,
            "isoWeek": f"{week_num} неделя ISO",
            "even": even,
            "data": week_data
        })

    return response

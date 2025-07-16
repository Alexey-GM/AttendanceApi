from datetime import date, timedelta
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from data.db.db import get_db
from data.models.attendance import Attendance
from data.models.schedule import Schedule
from data.models.student import Student
from data.models.student_group import StudentGroup
from sqlalchemy import case

router = APIRouter(prefix="/direction_summary")

DIRECTION_SHORT_NAMES = {
    "Прикладная информатика": "ПИ",
    "Математическое обеспечение и администрирование": "МОА",
    "Фундаментальная информатика": "ФИТ",
}

@router.get("/")
def direction_summary(period: str = Query(...), db: Session = Depends(get_db)):
    today = date.today()
    if period == "last_week":
        start_date = today - timedelta(days=today.weekday() + 7)
        end_date = start_date + timedelta(days=7)
    elif period == "last_month":
        start_date = (today.replace(day=1) - timedelta(days=1)).replace(day=1)
        end_date = today.replace(day=1)
    elif period.startswith("month_"): 
        month = int(period.split("_")[1])
        year = today.year
        start_date = date(year, month, 1)
        if month == 12:
            end_date = date(year + 1, 1, 1)
        else:
            end_date = date(year, month + 1, 1)
    else:
        raise HTTPException(status_code=400, detail="Неверный период")

    results = (
    db.query(
        StudentGroup.direction,
        func.count(case(
            (and_(Schedule.date >= start_date, Schedule.date < end_date), Attendance.id)
        )).label("total"),
        func.sum(case(
            (and_(Schedule.date >= start_date, Schedule.date < end_date, Attendance.status == 1), 1),
            else_=0
        )).label("present")
    )
    .outerjoin(Student, Student.group_id == StudentGroup.id)
    .outerjoin(Attendance, Attendance.student == Student.id)
    .outerjoin(Schedule, Schedule.id == Attendance.schedule)
    .group_by(StudentGroup.direction)
    .all()
    )
    response = [
    {
        "direction": DIRECTION_SHORT_NAMES.get(r.direction, r.direction),
        "attendance": round((r.present / r.total) * 100, 2) if r.total > 0 else 0.0
    }
    for r in results
    if r.total > 0
    ]

    return response


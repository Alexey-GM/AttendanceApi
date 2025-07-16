from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from service.attendance_chart_service import get_attendance_summary
from data.db.db import get_db

router = APIRouter(prefix="/attend", tags=["Attend"])

@router.get("/summary")
def attendance_summary(period: str, db: Session = Depends(get_db)):
    return get_attendance_summary(db, period)
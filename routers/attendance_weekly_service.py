from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from data.db.db import get_db
from service.attendance_weekly_service import get_weekly_attendance

router = APIRouter(prefix="/weekly", tags=["Weekly"])

@router.get("/")
def get_weekly_attendance_route(direction: str = None, course: int = None, db: Session = Depends(get_db)):
    return get_weekly_attendance(db, direction, course)

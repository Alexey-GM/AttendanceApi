from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from data.db.db import get_db
from service.student_attendance_service import get_student_weekly_attendance, get_all_students, get_subjects_for_student
router = APIRouter(prefix="/student_attendance", tags=["Student Attendance"])

@router.get("/")
def get_attendance(
    student_id: int = Query(...),
    subject_id: int = Query(...),
    type_class: str = Query(...),
    db: Session = Depends(get_db)
):
    return get_student_weekly_attendance(db, student_id, subject_id, type_class)

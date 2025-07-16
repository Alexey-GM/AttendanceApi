from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from data.db.db import get_db
from service.student_attendance_service import get_all_students, get_subjects_for_student

router = APIRouter(prefix="/student_subject", tags=["Students Subject"])

@router.get("/")
def get_students(db: Session = Depends(get_db)):
    return get_all_students(db)

@router.get("/{student_id}/subject")
def get_student_subjects(student_id: int, db: Session = Depends(get_db)):
    return get_subjects_for_student(db, student_id)

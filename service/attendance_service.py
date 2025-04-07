from sqlalchemy.orm import Session
from repository.attendance_repository import (
    get_all_attendance,
    get_attendance_by_id,
    create_attendance,
    update_attendance,
    delete_attendance
)

def fetch_all_attendance(db: Session):
    attendance_records = get_all_attendance(db)
    return [
        {
            "id": attendance.id,
            "schedule": attendance.schedule,
            "student": attendance.student,
            "status": attendance.status,
            "comment": attendance.comment
        }
        for attendance in attendance_records
    ] if attendance_records else []

def fetch_attendance_by_id(db: Session, attendance_id: int):
    attendance = get_attendance_by_id(db, attendance_id)
    if not attendance:
        return None
    return {
        "id": attendance.id,
        "schedule": attendance.schedule,
        "student": attendance.student,
        "status": attendance.status,
        "comment": attendance.comment
    }

def create_new_attendance(db: Session, attendance_data: dict):
    return create_attendance(db, attendance_data)

def update_existing_attendance(db: Session, attendance_id: int, attendance_data: dict):
    return update_attendance(db, attendance_id, attendance_data)

def delete_existing_attendance(db: Session, attendance_id: int):
    return delete_attendance(db, attendance_id)

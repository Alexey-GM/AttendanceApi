from sqlalchemy.orm import Session
from repository.attendance_repository import (
    get_all_attendance,
    get_attendance_by_id,
    create_attendance,
    update_attendance,
    delete_attendance
)

def fetch_all_attendance(db: Session):
    try:
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
    except Exception as e:
        raise ValueError(f"Service error fetching attendance: {str(e)}")

def fetch_attendance_by_id(db: Session, attendance_id: int):
    try:
        attendance = get_attendance_by_id(db, attendance_id)
        if not attendance:
            raise ValueError(f"Attendance with id {attendance_id} not found")
        return {
            "id": attendance.id,
            "schedule": attendance.schedule,
            "student": attendance.student,
            "status": attendance.status,
            "comment": attendance.comment
        }
    except Exception as e:
        raise ValueError(f"Service error fetching attendance: {str(e)}")

def create_new_attendance(db: Session, attendance_data: dict):
    try:
        required_fields = ["schedule", "student", "status"]
        if not all(field in attendance_data for field in required_fields):
            raise ValueError("Missing required fields")
            
        return create_attendance(db, attendance_data)
    except Exception as e:
        raise ValueError(f"Service error creating attendance: {str(e)}")

def update_existing_attendance(db: Session, attendance_id: int, attendance_data: dict):
    try:
        attendance = update_attendance(db, attendance_id, attendance_data)
        if not attendance:
            raise ValueError(f"Attendance with id {attendance_id} not found")
        return attendance
    except Exception as e:
        raise ValueError(f"Service error updating attendance: {str(e)}")

def delete_existing_attendance(db: Session, attendance_id: int):
    try:
        attendance = delete_attendance(db, attendance_id)
        if not attendance:
            raise ValueError(f"Attendance with id {attendance_id} not found")
        return attendance
    except Exception as e:
        raise ValueError(f"Service error deleting attendance: {str(e)}")

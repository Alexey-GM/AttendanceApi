from sqlalchemy.orm import Session
from data.models.attendance import Attendance
from sqlalchemy.exc import SQLAlchemyError

def get_all_attendance(db: Session):
    try:
        return db.query(Attendance).all()
    except SQLAlchemyError as e:
        raise ValueError(f"Error fetching attendance: {str(e)}")

def get_attendance_by_id(db: Session, attendance_id: int):
    try:
        attendance = db.query(Attendance).filter(Attendance.id == attendance_id).first()
        if not attendance:
            raise ValueError(f"Attendance with id {attendance_id} not found")
        return attendance
    except SQLAlchemyError as e:
        raise ValueError(f"Error fetching attendance: {str(e)}")

def create_attendance(db: Session, attendance_data: dict):
    try:
        new_attendance = Attendance(
            schedule=attendance_data["schedule"],
            student=attendance_data["student"],
            status=attendance_data["status"],
            comment=attendance_data.get("comment")
        )
        db.add(new_attendance)
        db.commit()
        db.refresh(new_attendance)
        return new_attendance
    except SQLAlchemyError as e:
        db.rollback()
        raise ValueError(f"Error creating attendance: {str(e)}")
    except KeyError as e:
        raise ValueError(f"Missing required field: {str(e)}")

def update_attendance(db: Session, attendance_id: int, attendance_data: dict):
    try:
        attendance = db.query(Attendance).filter(Attendance.id == attendance_id).first()
        if not attendance:
            raise ValueError(f"Attendance with id {attendance_id} not found")
        
        for key, value in attendance_data.items():
            setattr(attendance, key, value)
        
        db.commit()
        db.refresh(attendance)
        return attendance
    except SQLAlchemyError as e:
        db.rollback()
        raise ValueError(f"Error updating attendance: {str(e)}")

def delete_attendance(db: Session, attendance_id: int):
    try:
        attendance = db.query(Attendance).filter(Attendance.id == attendance_id).first()
        if not attendance:
            raise ValueError(f"Attendance with id {attendance_id} not found")
        
        db.delete(attendance)
        db.commit()
        return attendance
    except SQLAlchemyError as e:
        db.rollback()
        raise ValueError(f"Error deleting attendance: {str(e)}")
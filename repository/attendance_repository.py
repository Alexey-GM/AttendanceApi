from sqlalchemy.orm import Session
from data.models.attendance import Attendance

def get_all_attendance(db: Session):
    return db.query(Attendance).all()

def get_attendance_by_id(db: Session, attendance_id: int):
    return db.query(Attendance).filter(Attendance.id == attendance_id).first()

def create_attendance(db: Session, attendance_data: dict):
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

def update_attendance(db: Session, attendance_id: int, attendance_data: dict):
    attendance = db.query(Attendance).filter(Attendance.id == attendance_id).first()
    if not attendance:
        return None
    for key, value in attendance_data.items():
        setattr(attendance, key, value)
    db.commit()
    db.refresh(attendance)
    return attendance

def delete_attendance(db: Session, attendance_id: int):
    attendance = db.query(Attendance).filter(Attendance.id == attendance_id).first()
    if not attendance:
        return None
    db.delete(attendance)
    db.commit()
    return attendance

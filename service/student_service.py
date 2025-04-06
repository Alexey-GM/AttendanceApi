from sqlalchemy.orm import Session
from repository.student_repository import (
    get_all_students,
    get_student_by_id,
    create_student,
    update_student,
    delete_student
)

def fetch_all_students(db: Session):
    students = get_all_students(db)
    return [
        {
            "id": student.id,
            "first_name": student.first_name,
            "last_name": student.last_name,
            "middle_name": student.middle_name,
            "date_birth": student.date_birth.isoformat() if student.date_birth else None,
            "group_id": student.group_id
        }
        for student in students
    ] if students else []

def fetch_student_by_id(db: Session, student_id: int):
    student = get_student_by_id(db, student_id)
    if not student:
        return None
    return {
        "id": student.id,
        "first_name": student.first_name,
        "last_name": student.last_name,
        "middle_name": student.middle_name,
        "date_birth": student.date_birth.isoformat() if student.date_birth else None,
        "group_id": student.group_id
    }

def create_new_student(db: Session, student_data: dict):
    return create_student(db, student_data)

def update_existing_student(db: Session, student_id: int, student_data: dict):
    return update_student(db, student_id, student_data)

def delete_existing_student(db: Session, student_id: int):
    return delete_student(db, student_id)

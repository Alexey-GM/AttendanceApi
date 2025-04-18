from sqlalchemy.orm import Session
from repository.student_repository import (
    get_all_students,
    get_student_by_id,
    create_student,
    update_student,
    delete_student
)

def fetch_all_students(db: Session):
    try:
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
    except Exception as e:
        raise ValueError(f"Service error fetching students: {str(e)}")

def fetch_student_by_id(db: Session, student_id: int):
    try:
        student = get_student_by_id(db, student_id)
        if not student:
            raise ValueError(f"Student with id {student_id} not found")
        return {
            "id": student.id,
            "first_name": student.first_name,
            "last_name": student.last_name,
            "middle_name": student.middle_name,
            "date_birth": student.date_birth.isoformat() if student.date_birth else None,
            "group_id": student.group_id
        }
    except Exception as e:
        raise ValueError(f"Service error fetching student: {str(e)}")

def create_new_student(db: Session, student_data: dict):
    try:
        required_fields = ["first_name", "last_name", "group_id"]
        if not all(field in student_data for field in required_fields):
            raise ValueError("Missing required fields")
            
        return create_student(db, student_data)
    except Exception as e:
        raise ValueError(f"Service error creating student: {str(e)}")

def update_existing_student(db: Session, student_id: int, student_data: dict):
    try:
        student = update_student(db, student_id, student_data)
        if not student:
            raise ValueError(f"Student with id {student_id} not found")
        return student
    except Exception as e:
        raise ValueError(f"Service error updating student: {str(e)}")

def delete_existing_student(db: Session, student_id: int):
    try:
        student = delete_student(db, student_id)
        if not student:
            raise ValueError(f"Student with id {student_id} not found")
        return student
    except Exception as e:
        raise ValueError(f"Service error deleting student: {str(e)}")

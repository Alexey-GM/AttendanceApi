from sqlalchemy.orm import Session
from data.models.student import Student
from sqlalchemy.exc import SQLAlchemyError

def get_all_students(db: Session):
    try:
        return db.query(Student).all()
    except SQLAlchemyError as e:
        raise ValueError(f"Error fetching students: {str(e)}")

def get_student_by_id(db: Session, student_id: int):
    try:
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise ValueError(f"Student with id {student_id} not found")
        return student
    except SQLAlchemyError as e:
        raise ValueError(f"Error fetching student: {str(e)}")

def create_student(db: Session, student_data: dict):
    try:
        new_student = Student(
            first_name=student_data["first_name"],
            last_name=student_data["last_name"],
            middle_name=student_data.get("middle_name"),
            date_birth=student_data.get("date_birth"),
            group_id=student_data["group_id"]
        )
        db.add(new_student)
        db.commit()
        db.refresh(new_student)
        return new_student
    except SQLAlchemyError as e:
        db.rollback()
        raise ValueError(f"Error creating student: {str(e)}")
    except KeyError as e:
        raise ValueError(f"Missing required field: {str(e)}")

def update_student(db: Session, student_id: int, student_data: dict):
    try:
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise ValueError(f"Student with id {student_id} not found")
        
        for key, value in student_data.items():
            setattr(student, key, value)
        
        db.commit()
        db.refresh(student)
        return student
    except SQLAlchemyError as e:
        db.rollback()
        raise ValueError(f"Error updating student: {str(e)}")

def delete_student(db: Session, student_id: int):
    try:
        student = db.query(Student).filter(Student.id == student_id).first()
        if not student:
            raise ValueError(f"Student with id {student_id} not found")
        
        db.delete(student)
        db.commit()
        return student
    except SQLAlchemyError as e:
        db.rollback()
        raise ValueError(f"Error deleting student: {str(e)}")

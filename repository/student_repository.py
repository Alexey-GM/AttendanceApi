from sqlalchemy.orm import Session
from data.models.student import Student

def get_all_students(db: Session):
    return db.query(Student).all()

def get_student_by_id(db: Session, student_id: int):
    return db.query(Student).filter(Student.id == student_id).first()

def create_student(db: Session, student_data: dict):
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

def update_student(db: Session, student_id: int, student_data: dict):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        return None
    for key, value in student_data.items():
        setattr(student, key, value)
    db.commit()
    db.refresh(student)
    return student

def delete_student(db: Session, student_id: int):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        return None
    db.delete(student)
    db.commit()
    return student

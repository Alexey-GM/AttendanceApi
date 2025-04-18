from sqlalchemy.orm import Session
from data.models.subject import Subject
from sqlalchemy.exc import SQLAlchemyError

def get_all_subjects(db: Session):
    try:
        return db.query(Subject).all()
    except SQLAlchemyError as e:
        raise ValueError(f"Error fetching subjects: {str(e)}")

def get_subject_by_id(db: Session, subject_id: int):
    try:
        subject = db.query(Subject).filter(Subject.id == subject_id).first()
        if not subject:
            raise ValueError(f"Subject with id {subject_id} not found")
        return subject
    except SQLAlchemyError as e:
        raise ValueError(f"Error fetching subject: {str(e)}")

def create_subject(db: Session, subject_data: dict):
    try:
        if subject_data.get("teacher_id") is None:
            raise ValueError("Teacher ID must not be None")
        
        new_subject = Subject(
            name=subject_data["name"],
            teacher_id=subject_data["teacher_id"],
            hours=subject_data.get("hours")
        )
        db.add(new_subject)
        db.commit()
        db.refresh(new_subject)
        return new_subject
    except SQLAlchemyError as e:
        db.rollback()
        raise ValueError(f"Error creating subject: {str(e)}")
    except KeyError as e:
        raise ValueError(f"Missing required field: {str(e)}")

def update_subject(db: Session, subject_id: int, subject_data: dict):
    try:
        subject = db.query(Subject).filter(Subject.id == subject_id).first()
        if not subject:
            raise ValueError(f"Subject with id {subject_id} not found")
        
        for key, value in subject_data.items():
            if key == "teacher_id":
                setattr(subject, "teacher_id", value)
            else:
                setattr(subject, key, value)
        
        db.commit()
        db.refresh(subject)
        return subject
    except SQLAlchemyError as e:
        db.rollback()
        raise ValueError(f"Error updating subject: {str(e)}")

def delete_subject(db: Session, subject_id: int):
    try:
        subject = db.query(Subject).filter(Subject.id == subject_id).first()
        if not subject:
            raise ValueError(f"Subject with id {subject_id} not found")
        
        db.delete(subject)
        db.commit()
        return subject
    except SQLAlchemyError as e:
        db.rollback()
        raise ValueError(f"Error deleting subject: {str(e)}")
from sqlalchemy.orm import Session
from repository.subject_repository import (
    get_all_subjects,
    get_subject_by_id,
    create_subject,
    update_subject,
    delete_subject,
    get_subjects_by_teacher_id
)

def fetch_all_subjects(db: Session):
    subjects = get_all_subjects(db)
    return [
        {
            "id": subject.id,
            "name": subject.name,
            "lecturer": subject.lecturer,
            "hours": subject.hours
        }
        for subject in subjects
    ] if subjects else []

def fetch_subject_by_id(db: Session, subject_id: int):
    subject = get_subject_by_id(db, subject_id)
    if not subject:
        return None
    return {
        "id": subject.id,
        "name": subject.name,
        "lecturer": subject.lecturer, 
        "hours": subject.hours
    }

def create_new_subject(db: Session, subject_data: dict):
    try:
        required_fields = ["name", "teacher_id"]
        if not all(field in subject_data for field in required_fields):
            raise ValueError("Missing required fields")
            
        return create_subject(db, subject_data)
    except Exception as e:
        raise ValueError(f"Service error creating subject: {str(e)}")

def update_existing_subject(db: Session, subject_id: int, subject_data: dict):
    try:
        subject = update_subject(db, subject_id, subject_data)
        if not subject:
            raise ValueError(f"Subject with id {subject_id} not found")
        return subject
    except Exception as e:
        raise ValueError(f"Service error updating subject: {str(e)}")

def delete_existing_subject(db: Session, subject_id: int):
    return delete_subject(db, subject_id)
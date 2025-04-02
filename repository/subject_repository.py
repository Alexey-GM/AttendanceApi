from sqlalchemy.orm import Session
from data.models.subject import Subject

def get_all_subjects(db: Session):
    return db.query(Subject).all()

def get_subject_by_id(db: Session, subject_id: int):
    return db.query(Subject).filter(Subject.id == subject_id).first()

def create_subject(db: Session, subject_data: dict):
    new_subject = Subject(**subject_data)
    db.add(new_subject)
    db.commit()
    db.refresh(new_subject)
    return new_subject

def update_subject(db: Session, subject_id: int, subject_data: dict):
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not subject:
        return None
    for key, value in subject_data.items():
        setattr(subject, key, value)
    db.commit()
    db.refresh(subject)
    return subject

def delete_subject(db: Session, subject_id: int):
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not subject:
        return None
    db.delete(subject)
    db.commit()
    return subject
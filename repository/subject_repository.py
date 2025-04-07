from sqlalchemy.orm import Session
from data.models.subject import Subject

def get_all_subjects(db: Session):
    return db.query(Subject).all()

def get_subject_by_id(db: Session, subject_id: int):
    return db.query(Subject).filter(Subject.id == subject_id).first()

def create_subject(db: Session, subject_data: dict):
    if subject_data.get("lecturer") is None:
        raise ValueError("Lecturer ID must not be None")
    
    new_subject = Subject(
        name=subject_data["name"],
        lecturer=subject_data["lecturer"], 
        hours=subject_data.get("hours")
    )
    db.add(new_subject)
    db.commit()
    db.refresh(new_subject)
    return new_subject

def update_subject(db: Session, subject_id: int, subject_data: dict):
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not subject:
        return None
    for key, value in subject_data.items():
        if key == "lecturer": 
            setattr(subject, "lecturer", value)
        else:
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
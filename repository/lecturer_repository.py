from sqlalchemy.orm import Session
from data.models.lecturer import Lecturer

def get_all_lecturer(db: Session):
    return db.query(Lecturer).all()

def get_lecturer_by_id(db: Session, lecturer_id: int):
    return db.query(Lecturer).filter(Lecturer.id == lecturer_id).first()

def create_lecturer(db: Session, lecturer_data: dict):
    new_lecturer = Lecturer(**lecturer_data)
    db.add(new_lecturer)
    db.commit()
    db.refresh(new_lecturer)
    return new_lecturer

def update_lecturer(db: Session, lecturer_id: int, lecturer_data: dict):
    lecturer = db.query(Lecturer).filter(Lecturer.id == lecturer_id).first()
    if not lecturer:
        return None
    
    for key, value in lecturer_data.items():
        setattr(lecturer, key, value)
    
    db.commit()
    db.refresh(lecturer)  
    return lecturer 

def delete_lecturer(db: Session, lecturer_id: int):
    lecturer = db.query(Lecturer).filter(Lecturer.id == lecturer_id).first()
    if not lecturer:
        return None
    
    db.delete(lecturer)
    db.commit() 
    return lecturer
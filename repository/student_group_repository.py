from sqlalchemy.orm import Session
from data.models.student_group import StudentGroup

def get_all_student_groups(db: Session):
    return db.query(StudentGroup).all()

def get_student_group_by_id(db: Session, group_id: int):
    return db.query(StudentGroup).filter(StudentGroup.id == group_id).first()

def create_student_group(db: Session, group_data: dict):
    new_group = StudentGroup(**group_data)
    db.add(new_group)
    db.commit()
    db.refresh(new_group)
    return new_group

def update_student_group(db: Session, group_id: int, group_data: dict):
    group = db.query(StudentGroup).filter(StudentGroup.id == group_id).first()
    if not group:
        return None
    
    for key, value in group_data.items():
        setattr(group, key, value)
    
    db.commit()
    db.refresh(group)  
    return group 

def delete_student_group(db: Session, group_id: int):
    group = db.query(StudentGroup).filter(StudentGroup.id == group_id).first()
    if not group:
        return None
    
    db.delete(group)
    db.commit() 
    return group 
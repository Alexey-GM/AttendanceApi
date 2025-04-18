from sqlalchemy.orm import Session
from data.models.student_group import StudentGroup
from sqlalchemy.exc import SQLAlchemyError

def get_all_student_groups(db: Session):
    try:
        return db.query(StudentGroup).all()
    except SQLAlchemyError as e:
        raise ValueError(f"Error fetching student groups: {str(e)}")

def get_student_group_by_id(db: Session, group_id: int):
    try:
        group = db.query(StudentGroup).filter(StudentGroup.id == group_id).first()
        if not group:
            raise ValueError(f"Student group with id {group_id} not found")
        return group
    except SQLAlchemyError as e:
        raise ValueError(f"Error fetching student group: {str(e)}")

def create_student_group(db: Session, group_data: dict):
    try:
        new_group = StudentGroup(**group_data)
        db.add(new_group)
        db.commit()
        db.refresh(new_group)
        return new_group
    except SQLAlchemyError as e:
        db.rollback()
        raise ValueError(f"Error creating student group: {str(e)}")
    except TypeError as e:
        raise ValueError(f"Invalid data format: {str(e)}")

def update_student_group(db: Session, group_id: int, group_data: dict):
    try:
        group = db.query(StudentGroup).filter(StudentGroup.id == group_id).first()
        if not group:
            raise ValueError(f"Student group with id {group_id} not found")
        
        for key, value in group_data.items():
            setattr(group, key, value)
        
        db.commit()
        db.refresh(group)
        return group
    except SQLAlchemyError as e:
        db.rollback()
        raise ValueError(f"Error updating student group: {str(e)}")

def delete_student_group(db: Session, group_id: int):
    try:
        group = db.query(StudentGroup).filter(StudentGroup.id == group_id).first()
        if not group:
            raise ValueError(f"Student group with id {group_id} not found")
        
        db.delete(group)
        db.commit()
        return group
    except SQLAlchemyError as e:
        db.rollback()
        raise ValueError(f"Error deleting student group: {str(e)}")
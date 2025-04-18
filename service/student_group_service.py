from sqlalchemy.orm import Session
from repository.student_group_repository import (
    get_all_student_groups,
    get_student_group_by_id,
    create_student_group,
    update_student_group,
    delete_student_group
)

def fetch_all_student_groups(db: Session):
    try:
        groups = get_all_student_groups(db)
        return [
            {
                "id": group.id,
                "name": group.name,
                "direction": group.direction,
                "course": group.course
            }
            for group in groups
        ] if groups else []
    except Exception as e:
        raise ValueError(f"Service error fetching student groups: {str(e)}")

def fetch_student_group_by_id(db: Session, group_id: int):
    try:
        group = get_student_group_by_id(db, group_id)
        if not group:
            raise ValueError(f"Student group with id {group_id} not found")
        return {
            "id": group.id,
            "name": group.name,
            "direction": group.direction,
            "course": group.course
        }
    except Exception as e:
        raise ValueError(f"Service error fetching student group: {str(e)}")

def create_new_student_group(db: Session, group_data: dict):
    try:
        if not group_data.get("name"):
            raise ValueError("Group name is required")
            
        return create_student_group(db, group_data)
    except Exception as e:
        raise ValueError(f"Service error creating student group: {str(e)}")

def update_existing_student_group(db: Session, group_id: int, group_data: dict):
    try:
        group = update_student_group(db, group_id, group_data)
        if not group:
            raise ValueError(f"Student group with id {group_id} not found")
        return group
    except Exception as e:
        raise ValueError(f"Service error updating student group: {str(e)}")

def delete_existing_student_group(db: Session, group_id: int):
    try:
        group = delete_student_group(db, group_id)
        if not group:
            raise ValueError(f"Student group with id {group_id} not found")
        return group
    except Exception as e:
        raise ValueError(f"Service error deleting student group: {str(e)}")
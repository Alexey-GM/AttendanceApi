from sqlalchemy.orm import Session
from repository.student_group_repository import (
    get_all_student_groups,
    get_student_group_by_id,
    create_student_group,
    update_student_group,
    delete_student_group
)

def fetch_all_student_groups(db: Session):
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

def fetch_student_group_by_id(db: Session, group_id: int):
    group = get_student_group_by_id(db, group_id)
    if not group:
        return None
    return {
        "id": group.id,
        "name": group.name,
        "direction": group.direction,
        "course": group.course
    }

def create_new_student_group(db: Session, group_data: dict):
    return create_student_group(db, group_data)

def update_existing_student_group(db: Session, group_id: int, group_data: dict):
    return update_student_group(db, group_id, group_data)

def delete_existing_student_group(db: Session, group_id: int):
    return delete_student_group(db, group_id)
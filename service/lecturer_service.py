from sqlalchemy.orm import Session
from repository.lecturer_repository import (
    get_all_lecturer,
    get_lecturer_by_id,
    create_lecturer,
    update_lecturer,
    delete_lecturer
)

def fetch_all_lecturers(db: Session):
    lecturers = get_all_lecturer(db)
    return [
        {
            "id": lecturer.id,
            "first_name": lecturer.first_name,
            "last_name": lecturer.last_name,
            "middle_name": lecturer.middle_name,
            "date_birth": lecturer.date_birth.isoformat(),
            "phone": lecturer.phone
        }
        for lecturer in lecturers
    ] if lecturers else []

def fetch_lecturer_by_id(db: Session, lecturer_id: int):
    lecturer = get_lecturer_by_id(db, lecturer_id)
    if not lecturer:
        return None
    return {
        "id": lecturer.id,
        "first_name": lecturer.first_name,
        "last_name": lecturer.last_name,
        "middle_name": lecturer.middle_name,
        "date_birth": lecturer.date_birth.isoformat(),
        "phone": lecturer.phone
    }

def create_new_lecturer(db: Session, lecturer_data: dict):
    return create_lecturer(db, lecturer_data)

def update_existing_lecturer(db: Session, lecturer_id: int, lecturer_data: dict):
    return update_lecturer(db, lecturer_id, lecturer_data)

def delete_existing_lecturer(db: Session, lecturer_id: int):
    return delete_lecturer(db, lecturer_id)

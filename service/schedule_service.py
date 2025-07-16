from sqlalchemy.orm import Session
from repository.schedule_repository import (
    get_all_schedules,
    get_schedule_by_id,
    create_schedule,
    update_schedule,
    delete_schedule
)
from repository.subject_repository import get_subject_by_id
from repository.student_group_repository import get_student_group_by_id
from data.db.schemas import SubjectResponse, StudentGroupResponse

def fetch_all_schedules(db: Session):
    schedules = get_all_schedules(db)
    return [
        {
            "id": schedule.id,
            "student_subject": schedule.student_subject,
            "group_id": schedule.group_id,
            "date": schedule.date.isoformat(),
            "classroom": schedule.classroom,
            "type_class": schedule.type_class,
            "start_time": schedule.start_time.isoformat(),
            "end_time": schedule.end_time.isoformat()
        }
        for schedule in schedules
    ] if schedules else []

def fetch_schedule_by_id(db: Session, schedule_id: int):
    schedule = get_schedule_by_id(db, schedule_id)
    if not schedule:
        return None
    return {
        "id": schedule.id,
        "student_subject": schedule.student_subject,
        "group_id": schedule.group_id,
        "date": schedule.date.isoformat(),
        "classroom": schedule.classroom,
        "type_class": schedule.type_class,
        "start_time": schedule.start_time.isoformat(),
        "end_time": schedule.end_time.isoformat()
    }

def create_new_schedule(db: Session, schedule_data: dict):
    return create_schedule(db, schedule_data)

def update_existing_schedule(db: Session, schedule_id: int, schedule_data: dict):
    return update_schedule(db, schedule_id, schedule_data)

def delete_existing_schedule(db: Session, schedule_id: int):
    return delete_schedule(db, schedule_id)

def fetch_schedules_by_subject_id(db: Session, subject_id: int):
    subject = get_subject_by_id(db, subject_id)
    if not subject:
        return None
    schedules = db.query(get_all_schedules(db)[0].__class__).filter_by(student_subject=subject_id).all()
    schedule_list = []
    for schedule in schedules:
        group = get_student_group_by_id(db, schedule.group_id)
        schedule_list.append({
            "id": schedule.id,
            "group": StudentGroupResponse.from_orm(group).dict(),
            "date": schedule.date.isoformat(),
            "classroom": schedule.classroom,
            "type_class": schedule.type_class,
            "start_time": schedule.start_time.isoformat(),
            "end_time": schedule.end_time.isoformat()
        })
    return {
        "subject": SubjectResponse.from_orm(subject).dict(),
        "schedule": schedule_list
    }

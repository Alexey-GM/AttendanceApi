from sqlalchemy.orm import Session
from repository.schedule_repository import (
    get_all_schedules,
    get_schedule_by_id,
    create_schedule,
    update_schedule,
    delete_schedule
)

def fetch_all_schedules(db: Session):
    try:
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
    except Exception as e:
        raise ValueError(f"Service error fetching schedules: {str(e)}")

def fetch_schedule_by_id(db: Session, schedule_id: int):
    try:
        schedule = get_schedule_by_id(db, schedule_id)
        if not schedule:
            raise ValueError(f"Schedule with id {schedule_id} not found")
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
    except Exception as e:
        raise ValueError(f"Service error fetching schedule: {str(e)}")

def create_new_schedule(db: Session, schedule_data: dict):
    try:
        required_fields = ["student_subject", "group_id", "date", "start_time", "end_time"]
        if not all(field in schedule_data for field in required_fields):
            raise ValueError("Missing required fields")
            
        return create_schedule(db, schedule_data)
    except Exception as e:
        raise ValueError(f"Service error creating schedule: {str(e)}")

def update_existing_schedule(db: Session, schedule_id: int, schedule_data: dict):
    try:
        schedule = update_schedule(db, schedule_id, schedule_data)
        if not schedule:
            raise ValueError(f"Schedule with id {schedule_id} not found")
        return schedule
    except Exception as e:
        raise ValueError(f"Service error updating schedule: {str(e)}")

def delete_existing_schedule(db: Session, schedule_id: int):
    try:
        schedule = delete_schedule(db, schedule_id)
        if not schedule:
            raise ValueError(f"Schedule with id {schedule_id} not found")
        return schedule
    except Exception as e:
        raise ValueError(f"Service error deleting schedule: {str(e)}")
from sqlalchemy.orm import Session
from data.models.schedule import Schedule

def get_all_schedules(db: Session):
    return db.query(Schedule).all()

def get_schedule_by_id(db: Session, schedule_id: int):
    return db.query(Schedule).filter(Schedule.id == schedule_id).first()

def create_schedule(db: Session, schedule_data: dict):
    new_schedule = Schedule(
        student_subject=schedule_data["student_subject"],
        group_id=schedule_data["group_id"],
        date=schedule_data["date"],
        classroom=schedule_data.get("classroom"),
        type_class=schedule_data.get("type_class"),
        start_time=schedule_data["start_time"],
        end_time=schedule_data["end_time"]
    )
    db.add(new_schedule)
    db.commit()
    db.refresh(new_schedule)
    return new_schedule

def update_schedule(db: Session, schedule_id: int, schedule_data: dict):
    schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()
    if not schedule:
        return None
    for key, value in schedule_data.items():
        setattr(schedule, key, value)
    db.commit()
    db.refresh(schedule)
    return schedule

def delete_schedule(db: Session, schedule_id: int):
    schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()
    if not schedule:
        return None
    db.delete(schedule)
    db.commit()
    return schedule

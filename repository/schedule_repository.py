from sqlalchemy.orm import Session
from data.models.schedule import Schedule
from sqlalchemy.exc import SQLAlchemyError

def get_all_schedules(db: Session):
    try:
        return db.query(Schedule).all()
    except SQLAlchemyError as e:
        raise ValueError(f"Error fetching schedules: {str(e)}")

def get_schedule_by_id(db: Session, schedule_id: int):
    try:
        schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()
        if not schedule:
            raise ValueError(f"Schedule with id {schedule_id} not found")
        return schedule
    except SQLAlchemyError as e:
        raise ValueError(f"Error fetching schedule: {str(e)}")

def create_schedule(db: Session, schedule_data: dict):
    try:
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
    except SQLAlchemyError as e:
        db.rollback()
        raise ValueError(f"Error creating schedule: {str(e)}")
    except KeyError as e:
        raise ValueError(f"Missing required field: {str(e)}")

def update_schedule(db: Session, schedule_id: int, schedule_data: dict):
    try:
        schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()
        if not schedule:
            raise ValueError(f"Schedule with id {schedule_id} not found")
        
        for key, value in schedule_data.items():
            setattr(schedule, key, value)
        
        db.commit()
        db.refresh(schedule)
        return schedule
    except SQLAlchemyError as e:
        db.rollback()
        raise ValueError(f"Error updating schedule: {str(e)}")

def delete_schedule(db: Session, schedule_id: int):
    try:
        schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()
        if not schedule:
            raise ValueError(f"Schedule with id {schedule_id} not found")
        
        db.delete(schedule)
        db.commit()
        return schedule
    except SQLAlchemyError as e:
        db.rollback()
        raise ValueError(f"Error deleting schedule: {str(e)}")

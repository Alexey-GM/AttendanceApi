from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from data.db.db import get_db
from pydantic import BaseModel
from typing import Optional, List
from service.schedule_service import (
    fetch_all_schedules,
    fetch_schedule_by_id,
    create_new_schedule,
    update_existing_schedule,
    delete_existing_schedule
)
from data.response import format_response
import logging

class ScheduleResponse(BaseModel):
    id: int
    student_subject: int
    group_id: int
    date: str
    classroom: Optional[str] = None
    type_class: Optional[str] = None
    start_time: str
    end_time: str  

class SchedulesResponse(BaseModel):
    timestamp: str
    message: str
    code: int
    data: List[ScheduleResponse]

class ScheduleResponseWrapper(BaseModel):
    timestamp: str
    message: str
    code: int
    data: Optional[ScheduleResponse]

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/schedule", tags=["schedule"])

@router.get("/", response_model=SchedulesResponse)
def read_schedules(db: Session = Depends(get_db)):
    try:
        logger.info("Fetching all schedules")
        schedules = fetch_all_schedules(db)
        return format_response(data=schedules, message="Schedules retrieved successfully", code=200)
    except Exception as e:
        logger.exception("Error while fetching schedules")
        raise HTTPException(status_code=500, detail="Failed to retrieve schedules")

@router.get("/{schedule_id}", response_model=ScheduleResponseWrapper)
def read_schedule(schedule_id: int, db: Session = Depends(get_db)):
    try:
        logger.info(f"Fetching schedule with ID: {schedule_id}")
        schedule = fetch_schedule_by_id(db, schedule_id)
        if not schedule:
            logger.warning(f"Schedule with ID {schedule_id} not found")
            raise HTTPException(status_code=404, detail="Schedule not found")
        return format_response(data=schedule, message="Schedule retrieved successfully", code=200)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.exception(f"Error while fetching schedule ID {schedule_id}")
        raise HTTPException(status_code=500, detail="Failed to retrieve schedule")

@router.post("/", response_model=ScheduleResponseWrapper)
def create_schedule(schedule: dict, db: Session = Depends(get_db)):
    try:
        logger.info("Creating a new schedule")
        new_schedule = create_new_schedule(db, schedule)
        new_schedule_response = {
            "id": new_schedule.id,
            "student_subject": new_schedule.student_subject,
            "group_id": new_schedule.group_id,
            "date": new_schedule.date.isoformat(),
            "classroom": new_schedule.classroom,
            "type_class": new_schedule.type_class,
            "start_time": new_schedule.start_time.isoformat(),
            "end_time": new_schedule.end_time.isoformat()
        }
        return format_response(data=new_schedule_response, message="Schedule created successfully", code=201)
    except Exception as e:
        logger.exception("Error while creating schedule")
        raise HTTPException(status_code=500, detail="Failed to create schedule")

@router.put("/{schedule_id}", response_model=ScheduleResponseWrapper)
def update_schedule(schedule_id: int, schedule: dict, db: Session = Depends(get_db)):
    try:
        logger.info(f"Updating schedule ID: {schedule_id}")
        updated_schedule = update_existing_schedule(db, schedule_id, schedule)
        if not updated_schedule:
            logger.warning(f"Schedule with ID {schedule_id} not found for update")
            raise HTTPException(status_code=404, detail="Schedule not found")

        updated_schedule_response = {
            "id": updated_schedule.id,
            "student_subject": updated_schedule.student_subject,
            "group_id": updated_schedule.group_id,
            "date": updated_schedule.date.isoformat(),
            "classroom": updated_schedule.classroom,
            "type_class": updated_schedule.type_class,
            "start_time": updated_schedule.start_time.isoformat(),
            "end_time": updated_schedule.end_time.isoformat()
        }
        return format_response(data=updated_schedule_response, message="Schedule updated successfully", code=200)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.exception(f"Error while updating schedule ID {schedule_id}")
        raise HTTPException(status_code=500, detail="Failed to update schedule")

@router.delete("/{schedule_id}", response_model=dict)
def delete_schedule(schedule_id: int, db: Session = Depends(get_db)):
    try:
        logger.info(f"Deleting schedule ID: {schedule_id}")
        deleted_schedule = delete_existing_schedule(db, schedule_id)
        if not deleted_schedule:
            logger.warning(f"Schedule with ID {schedule_id} not found for deletion")
            raise HTTPException(status_code=404, detail="Schedule not found")
        return format_response(data=None, message="Schedule deleted successfully", code=200)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.exception(f"Error while deleting schedule ID {schedule_id}")
        raise HTTPException(status_code=500, detail="Failed to delete schedule")


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
    delete_existing_schedule,
    fetch_schedules_by_subject_id,
    batch_create_schedules_service
)
from data.db.schemas import ScheduleWithDetailsResponse, ScheduleWrapperResponse, CreateScheduleList
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

class SchedulesWithDetailsResponse(BaseModel):
    timestamp: str
    message: str
    code: int
    data: List[ScheduleWithDetailsResponse]

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/schedule", tags=["schedule"])

@router.get("/", response_model=SchedulesResponse)
def read_schedules(db: Session = Depends(get_db)):
    logger.info("Fetching all schedules")
    schedules = fetch_all_schedules(db)
    return format_response(data=schedules, message="Schedules retrieved successfully", code=200)

@router.get("/{schedule_id}", response_model=ScheduleResponseWrapper)
def read_schedule(schedule_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching schedule with ID: {schedule_id}")
    schedule = fetch_schedule_by_id(db, schedule_id)
    
    if not schedule:
        logger.error(f"Schedule with ID {schedule_id} not found")
        raise HTTPException(status_code=404, detail="Schedule not found")
    
    return format_response(data=schedule, message="Schedule retrieved successfully", code=200)

@router.post("/", response_model=ScheduleResponseWrapper)
def create_schedule(new_schedules: CreateScheduleList, db: Session = Depends(get_db)):
    try:
        schedules_data = [item.model_dump() for item in new_schedules.root]
        created = batch_create_schedules_service(db, schedules_data)
        response_data = [
            {
                "id": s.id,
                "student_subject": s.student_subject,
                "group_id": s.group_id,
                "date": s.date.isoformat(),
                "classroom": s.classroom,
                "type_class": s.type_class,
                "start_time": s.start_time.isoformat(),
                "end_time": s.end_time.isoformat()
            }
            for s in created
        ]
        return format_response(data=response_data, message="Schedules created successfully", code=201)
    except Exception as e:
        logger.error(f"Error while batch creating schedules: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put("/{schedule_id}", response_model=ScheduleResponseWrapper)
def update_schedule(schedule_id: int, schedule: dict, db: Session = Depends(get_db)):
    try:
        updated_schedule = update_existing_schedule(db, schedule_id, schedule)
        if not updated_schedule:
            logger.error(f"Schedule with ID {schedule_id} not found for update")
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
    except Exception as e:
        logger.error(f"Error while updating schedule with ID {schedule_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/{schedule_id}", response_model=dict)
def delete_schedule(schedule_id: int, db: Session = Depends(get_db)):
    logger.info(f"Deleting schedule with ID: {schedule_id}")
    deleted_schedule = delete_existing_schedule(db, schedule_id)
    
    if not deleted_schedule:
        logger.error(f"Schedule with ID {schedule_id} not found for deletion")
        raise HTTPException(status_code=404, detail="Schedule not found")
    
    return format_response(data=None, message="Schedule deleted successfully", code=200)

@router.get("/subject/{subject_id}", response_model=ScheduleWrapperResponse)
def get_schedules_by_subject_id(subject_id: int, db: Session = Depends(get_db)):
    try:
        result = fetch_schedules_by_subject_id(db, subject_id)
    except Exception as e:  
        logger.error(f"Error fetching schedules for subject ID {subject_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    return format_response(data=result, message="Schedules retrieved successfully", code=200)

@router.get("/{subject_id}/{group_id}")
def get_schedules_by_subject_and_group(subject_id: int, group_id: int, db: Session = Depends(get_db)):
    try:
        # Получаем все расписания по предмету
        result = fetch_schedules_by_subject_id(db, subject_id)
        if not result or "schedule" not in result:
            return format_response(data=[], message="No schedules found", code=200)
        # Фильтруем по группе
        filtered = [s for s in result["schedule"] if s["group"]["id"] == group_id]
        return format_response(data=filtered, message="Schedules retrieved successfully", code=200)
    except Exception as e:
        logger.error(f"Error fetching schedules for subject {subject_id} and group {group_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

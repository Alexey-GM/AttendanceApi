from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from data.db.db import get_db
from pydantic import BaseModel
from typing import Optional, List
from service.attendance_service import (
    fetch_all_attendance,
    fetch_attendance_by_id,
    create_new_attendance,
    update_existing_attendance,
    delete_existing_attendance
)
from data.response import format_response
import logging

class AttendanceResponse(BaseModel):
    id: int
    schedule: int
    student: int
    status: int
    comment: Optional[str] = None

class AttendanceResponseWrapper(BaseModel):
    timestamp: str
    message: str
    code: int
    data: Optional[AttendanceResponse]

class AttendancesResponse(BaseModel):
    timestamp: str
    message: str
    code: int
    data: List[AttendanceResponse]

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/attendance", tags=["attendance"])

@router.get("/", response_model=AttendancesResponse)
def read_attendance(db: Session = Depends(get_db)):
    logger.info("Fetching all attendance records")
    attendance_records = fetch_all_attendance(db)
    return format_response(data=attendance_records, message="Attendance records retrieved successfully", code=200)

@router.get("/{attendance_id}", response_model=AttendanceResponseWrapper)
def read_attendance(attendance_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching attendance record with ID: {attendance_id}")
    attendance = fetch_attendance_by_id(db, attendance_id)
    
    if not attendance:
        logger.error(f"Attendance record with ID {attendance_id} not found")
        raise HTTPException(status_code=404, detail="Attendance record not found")
    
    return format_response(data=attendance, message="Attendance record retrieved successfully", code=200)

@router.post("/", response_model=AttendanceResponseWrapper)
def create_attendance(attendance: dict, db: Session = Depends(get_db)):
    try:
        new_attendance = create_new_attendance(db, attendance)
        new_attendance_response = {
            "id": new_attendance.id,
            "schedule": new_attendance.schedule,
            "student": new_attendance.student,
            "status": new_attendance.status,
            "comment": new_attendance.comment
        }
        return format_response(data=new_attendance_response, message="Attendance record created successfully", code=201)
    except Exception as e:
        logger.error(f"Error while creating attendance record: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put("/{attendance_id}", response_model=AttendanceResponseWrapper)
def update_attendance(attendance_id: int, attendance: dict, db: Session = Depends(get_db)):
    try:
        updated_attendance = update_existing_attendance(db, attendance_id, attendance)
        if not updated_attendance:
            logger.error(f"Attendance record with ID {attendance_id} not found for update")
            raise HTTPException(status_code=404, detail="Attendance record not found")
        
        updated_attendance_response = {
            "id": updated_attendance.id,
            "schedule": updated_attendance.schedule,
            "student": updated_attendance.student,
            "status": updated_attendance.status,
            "comment": updated_attendance.comment
        }
        
        return format_response(data=updated_attendance_response, message="Attendance record updated successfully", code=200)
    except Exception as e:
        logger.error(f"Error while updating attendance record with ID {attendance_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/{attendance_id}", response_model=dict)
def delete_attendance(attendance_id: int, db: Session = Depends(get_db)):
    logger.info(f"Deleting attendance record with ID: {attendance_id}")
    deleted_attendance = delete_existing_attendance(db, attendance_id)
    
    if not deleted_attendance:
        logger.error(f"Attendance record with ID {attendance_id} not found for deletion")
        raise HTTPException(status_code=404, detail="Attendance record not found")
    
    return format_response(data=None, message="Attendance record deleted successfully", code=200)

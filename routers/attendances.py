from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from data.db.db import get_db
from pydantic import BaseModel
from typing import Optional, List
from routers.dependencies import get_current_user, verify_lecturer
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
def read_attendance(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    try:
        logger.info("Fetching all attendance records")
        attendance_records = fetch_all_attendance(db)
        return format_response(data=attendance_records, message="Attendance records retrieved successfully", code=200)
    except Exception as e:
        logger.exception("Error fetching attendance records")
        raise HTTPException(status_code=500, detail="Failed to fetch attendance records")

@router.get("/{attendance_id}", response_model=AttendanceResponseWrapper)
def read_attendance_by_id(attendance_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    try:
        logger.info(f"Fetching attendance record with ID: {attendance_id}")
        attendance = fetch_attendance_by_id(db, attendance_id)
        if not attendance:
            raise HTTPException(status_code=404, detail=f"Attendance with ID {attendance_id} not found")
        return format_response(data=attendance, message="Attendance record retrieved successfully", code=200)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.exception(f"Error fetching attendance record {attendance_id}")
        raise HTTPException(status_code=500, detail="Failed to fetch attendance record")

@router.post("/", response_model=AttendanceResponseWrapper)
def create_attendance(attendance: dict, db: Session = Depends(get_db), current_user: dict = Depends(verify_lecturer)):
    try:
        logger.info("Creating new attendance record")
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
        logger.exception("Error creating attendance record")
        raise HTTPException(status_code=500, detail="Failed to create attendance record")

@router.put("/{attendance_id}", response_model=AttendanceResponseWrapper)
def update_attendance(attendance_id: int, attendance: dict, db: Session = Depends(get_db), current_user: dict = Depends(verify_lecturer)):
    try:
        logger.info(f"Updating attendance record with ID {attendance_id}")
        updated = update_existing_attendance(db, attendance_id, attendance)
        if not updated:
            raise HTTPException(status_code=404, detail=f"Attendance with ID {attendance_id} not found")
        response = {
            "id": updated.id,
            "schedule": updated.schedule,
            "student": updated.student,
            "status": updated.status,
            "comment": updated.comment
        }
        return format_response(data=response, message="Attendance updated successfully", code=200)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.exception(f"Error updating attendance {attendance_id}")
        raise HTTPException(status_code=500, detail="Failed to update attendance")

@router.delete("/{attendance_id}", response_model=dict)
def delete_attendance(attendance_id: int, db: Session = Depends(get_db), current_user: dict = Depends(verify_lecturer)):
    try:
        logger.info(f"Deleting attendance record ID: {attendance_id}")
        deleted = delete_existing_attendance(db, attendance_id)
        if not deleted:
            raise HTTPException(status_code=404, detail=f"Attendance with ID {attendance_id} not found")
        return format_response(data=None, message="Attendance deleted successfully", code=200)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.exception(f"Error deleting attendance {attendance_id}")
        raise HTTPException(status_code=500, detail="Failed to delete attendance")


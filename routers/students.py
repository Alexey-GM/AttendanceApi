from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from data.db.db import get_db
from pydantic import BaseModel
from typing import Optional, List
from service.student_service import (
    fetch_all_students,
    fetch_student_by_id,
    create_new_student,
    update_existing_student,
    delete_existing_student
)
from data.response import format_response
import logging

class StudentResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    date_birth: Optional[str] = None
    group_id: int

class StudentsResponse(BaseModel):
    timestamp: str
    message: str
    code: int
    data: List[StudentResponse]

class StudentResponseWrapper(BaseModel):
    timestamp: str
    message: str
    code: int
    data: Optional[StudentResponse]

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/student", tags=["student"])

@router.get("/", response_model=StudentsResponse)
def read_students(db: Session = Depends(get_db)):
    logger.info("Fetching all students")
    students = fetch_all_students(db)
    return format_response(data=students, message="Students retrieved successfully", code=200)

@router.get("/{student_id}", response_model=StudentResponseWrapper)
def read_student(student_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching student with ID: {student_id}")
    student = fetch_student_by_id(db, student_id)
    
    if not student:
        logger.error(f"Student with ID {student_id} not found")
        raise HTTPException(status_code=404, detail="Student not found")
    
    return format_response(data=student, message="Student retrieved successfully", code=200)

@router.post("/", response_model=StudentResponseWrapper)
def create_student(student: dict, db: Session = Depends(get_db)):
    try:
        new_student = create_new_student(db, student)
        new_student_response = {
            "id": new_student.id,
            "first_name": new_student.first_name,
            "last_name": new_student.last_name,
            "middle_name": new_student.middle_name,
            "date_birth": new_student.date_birth.isoformat() if new_student.date_birth else None,
            "group_id": new_student.group_id
        }
        return format_response(data=new_student_response, message="Student created successfully", code=201)
    except Exception as e:
        logger.error(f"Error while creating student: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put("/{student_id}", response_model=StudentResponseWrapper)
def update_student(student_id: int, student: dict, db: Session = Depends(get_db)):
    try:
        updated_student = update_existing_student(db, student_id, student)
        if not updated_student:
            logger.error(f"Student with ID {student_id} not found for update")
            raise HTTPException(status_code=404, detail="Student not found")
        
        updated_student_response = {
            "id": updated_student.id,
            "first_name": updated_student.first_name,
            "last_name": updated_student.last_name,
            "middle_name": updated_student.middle_name,
            "date_birth": updated_student.date_birth.isoformat() if updated_student.date_birth else None,
            "group_id": updated_student.group_id
        }
        
        return format_response(data=updated_student_response, message="Student updated successfully", code=200)
    except Exception as e:
        logger.error(f"Error while updating student with ID {student_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/{student_id}", response_model=dict)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    logger.info(f"Deleting student with ID: {student_id}")
    deleted_student = delete_existing_student(db, student_id)
    
    if not deleted_student:
        logger.error(f"Student with ID {student_id} not found for deletion")
        raise HTTPException(status_code=404, detail="Student not found")
    
    return format_response(data=None, message="Student deleted successfully", code=200)

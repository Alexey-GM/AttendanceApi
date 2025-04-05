from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from data.db.db import get_db
from pydantic import BaseModel
from typing import Optional
from service.lecturer_service import (
    fetch_all_lecturers,
    fetch_lecturer_by_id,
    create_new_lecturer,
    update_existing_lecturer,
    delete_existing_lecturer
)
from data.response import format_response
import logging

class LecturerResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    middle_name: str
    date_birth: str 
    phone: str

class LecturersResponse(BaseModel):
    timestamp: str
    message: str
    code: int
    data: list[LecturerResponse]

class LecturerResponseWrapper(BaseModel):
    timestamp: str
    message: str
    code: int
    data: Optional[LecturerResponse]

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/lecturer", tags=["lecturer"])

@router.get("/", response_model=LecturersResponse)
def read_lecturers(db: Session = Depends(get_db)):
    logger.info("Fetching all lecturers")
    lecturers = fetch_all_lecturers(db)
    return format_response(data=lecturers, message="Success", code=200)

@router.get("/{lecturer_id}", response_model=LecturerResponseWrapper)
def read_lecturer(lecturer_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching lecturer with ID: {lecturer_id}")
    lecturer = fetch_lecturer_by_id(db, lecturer_id)
    
    if not lecturer:
        logger.error(f"Lecturer with ID {lecturer_id} not found")
        raise HTTPException(status_code=404, detail="Lecturer not found")
    return format_response(data=lecturer, message="Success", code=200)

@router.post("/", response_model=dict)
def create_lecturer(lecturer: dict, db: Session = Depends(get_db)):
    try:
        new_lecturer = create_new_lecturer(db, lecturer)
        
        new_lecturer_response = {
            "id": new_lecturer.id,
            "first_name": new_lecturer.first_name,
            "last_name": new_lecturer.last_name,
            "middle_name": new_lecturer.middle_name,
            "date_birth": new_lecturer.date_birth.isoformat(),  # Преобразование даты в строку
            "phone": new_lecturer.phone
        }
        
        return format_response(data=new_lecturer_response, message="Lecturer created successfully", code=201)
    except Exception as e:
        logger.error(f"Error while creating Lecturer: {e}")
        return format_response(data=None, message="Lecturer server error", code=500)

@router.put("/{lecturer_id}", response_model=dict)
def update_lecturer(lecturer_id: int, lecturer: dict, db: Session = Depends(get_db)):
    try:
        updated_lecturer = update_existing_lecturer(db, lecturer_id, lecturer)
        if not updated_lecturer:
            return format_response(data=None, message="Lecturer not found", code=404)
        
        updated_lecturer_response = {
            "id": updated_lecturer.id,
            "first_name": updated_lecturer.first_name,
            "last_name": updated_lecturer.last_name,
            "middle_name": updated_lecturer.middle_name,
            "date_birth": updated_lecturer.date_birth.isoformat(),  # Преобразование даты в строку
            "phone": updated_lecturer.phone
        }
        
        return format_response(data=updated_lecturer_response, message="Lecturer updated successfully", code=200)
    except Exception as e:
        logger.error(f"Error while updating Lecturer with ID {lecturer_id}: {e}")
        return format_response(data=None, message="Internal server error", code=500)

@router.delete("/{lecturer_id}", response_model=dict)
def delete_lecturer(lecturer_id: int, db: Session = Depends(get_db)):
    logger.info(f"Deleting lecturer with ID: {lecturer_id}")
    deleted_lecturer = delete_existing_lecturer(db, lecturer_id)
    
    if not deleted_lecturer:
        logger.error(f"Lecturer with ID {lecturer_id} not found for deletion")
        raise HTTPException(status_code=404, detail="Lecturer not found")
    
    return format_response(data=None, message="Lecturer deleted successfully", code=200)


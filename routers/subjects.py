from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from data.db.db import get_db
from pydantic import BaseModel
from typing import Optional, List
from service.subject_service import (
    fetch_all_subjects,
    fetch_subject_by_id,
    create_new_subject,
    update_existing_subject,
    delete_existing_subject
)
from data.response import format_response
import logging

class SubjectResponse(BaseModel):
    id: int
    name: str
    lecturer: int 
    hours: int

class SubjectsResponse(BaseModel):
    timestamp: str
    message: str
    code: int
    data: List[SubjectResponse]

class SubjectResponseWrapper(BaseModel):
    timestamp: str
    message: str
    code: int
    data: Optional[SubjectResponse]

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/subjects", tags=["subjects"])

@router.get("/", response_model=SubjectsResponse)
def read_subjects(db: Session = Depends(get_db)):
    logger.info("Fetching all subjects")
    subjects = fetch_all_subjects(db)
    return format_response(data=subjects, message="Subjects retrieved successfully", code=200)

@router.get("/{subject_id}", response_model=SubjectResponseWrapper)
def read_subject(subject_id: int, db: Session = Depends(get_db)):
    logger.info(f"Fetching subject with ID: {subject_id}")
    subject = fetch_subject_by_id(db, subject_id)
    
    if not subject:
        logger.error(f"Subject with ID {subject_id} not found")
        raise HTTPException(status_code=404, detail="Subject not found")
    
    return format_response(data=subject, message="Subject retrieved successfully", code=200)

@router.post("/", response_model=SubjectResponseWrapper)
def create_subject(subject: dict, db: Session = Depends(get_db)):
    try:
        new_subject = create_new_subject(db, subject)
        new_subject_response = {
            "id": new_subject.id,
            "name": new_subject.name,
            "lecturer": new_subject.lecturer,
            "hours": new_subject.hours
        }
        return format_response(data=new_subject_response, message="Subject created successfully", code=201)
    except Exception as e:
        logger.error(f"Error while creating subject: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.put("/{subject_id}", response_model=SubjectResponseWrapper)
def update_subject(subject_id: int, subject: dict, db: Session = Depends(get_db)):
    try:
        updated_subject = update_existing_subject(db, subject_id, subject)
        if not updated_subject:
            logger.error(f"Subject with ID {subject_id} not found for update")
            raise HTTPException(status_code=404, detail="Subject not found")
        
        updated_subject_response = {
            "id": updated_subject.id,
            "name": updated_subject.name,
            "lecturer": updated_subject.lecturer,
            "hours": updated_subject.hours
        }
        
        return format_response(data=updated_subject_response, message="Subject updated successfully", code=200)
    except Exception as e:
        logger.error(f"Error while updating subject with ID {subject_id}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.delete("/{subject_id}", response_model=dict)
def delete_subject(subject_id: int, db: Session = Depends(get_db)):
    logger.info(f"Deleting subject with ID: {subject_id}")
    deleted_subject = delete_existing_subject(db, subject_id)
    
    if not deleted_subject:
        logger.error(f"Subject with ID {subject_id} not found for deletion")
        raise HTTPException(status_code=404, detail="Subject not found")
    
    return format_response(data=None, message="Subject deleted successfully", code=200)

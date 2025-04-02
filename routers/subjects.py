from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from data.db.db import get_db
from service.subject_service import (
    fetch_all_subjects,
    fetch_subject_by_id,
    create_new_subject,
    update_existing_subject,
    delete_existing_subject
)
from data.response import format_response
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/subjects", tags=["subjects"])

@router.get("/", response_model=dict)
def read_subjects(db: Session = Depends(get_db)):
    try:
        subjects = fetch_all_subjects(db)
        return format_response(data=subjects, message="Subjects retrieved successfully", code=200)
    except Exception as e:
        logger.error(f"Error while retrieving subjects: {e}")
        return format_response(data=None, message="Internal server error", code=500)


@router.get("/{subject_id}", response_model=dict)
def read_subject(subject_id: int, db: Session = Depends(get_db)):
    try:
        subject = fetch_subject_by_id(db, subject_id)
        if not subject:
            return format_response(data=None, message="Subject not found", code=404)
        return format_response(data=subject, message="Subject retrieved successfully", code=200)
    except Exception as e:
        logger.error(f"Error while retrieving subject with ID {subject_id}: {e}")
        return format_response(data=None, message="Internal server error", code=500)


@router.post("/", response_model=dict)
def create_subject(subject: dict, db: Session = Depends(get_db)):
    try:
        new_subject = create_new_subject(db, subject)
        return format_response(data=new_subject, message="Subject created successfully", code=201)
    except Exception as e:
        logger.error(f"Error while creating subject: {e}")
        return format_response(data=None, message="Internal server error", code=500)


@router.put("/{subject_id}", response_model=dict)
def update_subject(subject_id: int, subject: dict, db: Session = Depends(get_db)):
    try:
        updated_subject = update_existing_subject(db, subject_id, subject)
        if not updated_subject:
            return format_response(data=None, message="Subject not found", code=404)
        return format_response(data=updated_subject, message="Subject updated successfully", code=200)
    except Exception as e:
        logger.error(f"Error while updating subject with ID {subject_id}: {e}")
        return format_response(data=None, message="Internal server error", code=500)


@router.delete("/{subject_id}", response_model=dict)
def delete_subject(subject_id: int, db: Session = Depends(get_db)):
    try:
        deleted_subject = delete_existing_subject(db, subject_id)
        if not deleted_subject:
            return format_response(data=None, message="Subject not found", code=404)
        return format_response(data=None, message="Subject deleted successfully", code=200)
    except Exception as e:
        logger.error(f"Error while deleting subject with ID {subject_id}: {e}")
        return format_response(data=None, message="Internal server error", code=500)
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from data.db.db import get_db
from pydantic import BaseModel
from typing import Optional, List
from routers.dependencies import get_current_user, verify_lecturer
from service.student_group_service import (
    fetch_all_student_groups,
    fetch_student_group_by_id,
    create_new_student_group,
    update_existing_student_group,
    delete_existing_student_group
)
from data.response import format_response
import logging

class StudentGroupResponse(BaseModel):
    id: int
    name: str
    direction: str
    course: int

class StudentGroupsResponse(BaseModel):
    timestamp: str
    message: str
    code: int
    data: List[StudentGroupResponse]

class StudentGroupResponseWrapper(BaseModel):
    timestamp: str
    message: str
    code: int
    data: Optional[StudentGroupResponse]

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/student_group", tags=["student_group"])

@router.get("/", response_model=StudentGroupsResponse)
def read_student_groups(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    try:
        logger.info("Fetching all student groups")
        groups = fetch_all_student_groups(db)
        return format_response(data=groups, message="Success", code=200)
    except Exception as e:
        logger.exception("Error while fetching student groups")
        raise HTTPException(status_code=500, detail="Failed to retrieve student groups")

@router.get("/{group_id}", response_model=StudentGroupResponseWrapper)
def read_student_group(group_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    try:
        logger.info(f"Fetching student group with ID: {group_id}")
        group = fetch_student_group_by_id(db, group_id)
        if not group:
            logger.warning(f"Student group with ID {group_id} not found")
            raise HTTPException(status_code=404, detail="Student group not found")
        return format_response(data=group, message="Success", code=200)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.exception(f"Error while fetching student group ID {group_id}")
        raise HTTPException(status_code=500, detail="Failed to retrieve student group")

@router.post("/", response_model=StudentGroupResponseWrapper)
def create_student_group(group: dict, db: Session = Depends(get_db), current_user: dict = Depends(verify_lecturer)):
    try:
        logger.info("Creating new student group")
        new_group = create_new_student_group(db, group)

        new_group_response = {
            "id": new_group.id,
            "name": new_group.name,
            "direction": new_group.direction,
            "course": new_group.course
        }

        return format_response(data=new_group_response, message="Group created successfully", code=201)
    except Exception as e:
        logger.exception("Error while creating student group")
        raise HTTPException(status_code=500, detail="Failed to create student group")

@router.put("/{group_id}", response_model=StudentGroupResponseWrapper)
def update_student_group(group_id: int, group: dict, db: Session = Depends(get_db), current_user: dict = Depends(verify_lecturer)):
    try:
        logger.info(f"Updating student group ID: {group_id}")
        updated_group = update_existing_student_group(db, group_id, group)
        if not updated_group:
            logger.warning(f"Student group with ID {group_id} not found for update")
            raise HTTPException(status_code=404, detail="Student group not found")

        updated_group_response = {
            "id": updated_group.id,
            "name": updated_group.name,
            "direction": updated_group.direction,
            "course": updated_group.course
        }

        return format_response(data=updated_group_response, message="Group updated successfully", code=200)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.exception(f"Error while updating student group ID {group_id}")
        raise HTTPException(status_code=500, detail="Failed to update student group")

@router.delete("/{group_id}", response_model=dict)
def delete_student_group(group_id: int, db: Session = Depends(get_db), current_user: dict = Depends(verify_lecturer)):
    try:
        logger.info(f"Deleting student group ID: {group_id}")
        deleted_group = delete_existing_student_group(db, group_id)
        if not deleted_group:
            logger.warning(f"Student group with ID {group_id} not found for deletion")
            raise HTTPException(status_code=404, detail="Student group not found")

        return format_response(data=None, message="Group deleted successfully", code=200)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.exception(f"Error while deleting student group ID {group_id}")
        raise HTTPException(status_code=500, detail="Failed to delete student group")


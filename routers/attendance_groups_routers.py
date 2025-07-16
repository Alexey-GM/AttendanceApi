from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from data.db.db import get_db
from service.attendance_groups_service import get_group_attendance

router = APIRouter(prefix="/attendance_group", tags=["attendance_group"])

@router.get("/by-groups")
def attendance_by_groups(
    start_date: date = Query(..., description="Дата начала недели"),
    end_date: date = Query(..., description="Дата конца недели"),
    course: Optional[int] = Query(None),
    direction: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    return get_group_attendance(db, start_date, end_date, course, direction)

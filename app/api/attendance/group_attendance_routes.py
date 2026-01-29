from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.session import get_db
from app.schemas.attendance import GroupAttendanceResponse
from app.services.group_attendance_service import get_group_attendance_stats
from app.utils.jwt import get_current_lecturer_id
from app.utils.response import format_response

router = APIRouter(prefix="/group-attendance", tags=["group-attendance"])

@router.get("/", response_model=GroupAttendanceResponse)
async def get_group_attendance_statistics(
    course_number: int = Query(..., description="Номер курса", ge=1, le=6),
    track_name: str = Query(..., description="Название направления (например, ПИ, ФИТ, МОА)"),
    weeks_count: int = Query(default=4, description="Количество недель для анализа", ge=1, le=12),
    current_lecturer_id: int = Depends(get_current_lecturer_id),
    db: AsyncSession = Depends(get_db)
):
    """
    Получить статистику посещаемости по группам для указанного курса и направления
    
    - **course_number**: Номер курса (1-6)
    - **track_name**: Название направления (например, ПИ, ФИТ, МОА)
    - **weeks_count**: Количество недель для анализа (по умолчанию 4)
    """
    try:
        weeks = await get_group_attendance_stats(
            db, 
            course_number=course_number, 
            track_name=track_name,
            weeks_count=weeks_count
        )
        
        if not weeks:
            return format_response(
                data={"weeks": []},
                message=f"No groups found for course {course_number} and direction {track_name}",
                code=200
            )
        
        return format_response(
            data={"weeks": weeks},
            message=f"Group attendance statistics retrieved successfully for course {course_number}, direction {track_name}",
            code=200
        )
        
    except Exception as e:
        return format_response(
            message=str(e),
            code=400
        )




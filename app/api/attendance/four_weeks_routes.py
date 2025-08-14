from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.session import get_db
from app.schemas.attendance import FourWeeksAttendanceResponse
from app.services.four_weeks_attendance_service import get_four_weeks_attendance_stats
from app.utils.jwt import get_current_lecturer_id
from app.utils.response import format_response

router = APIRouter(prefix="/four-weeks", tags=["four-weeks"])

@router.get("/", response_model=FourWeeksAttendanceResponse)
async def get_four_weeks_attendance_statistics(
    course_number: int = Query(..., description="Номер курса", ge=1, le=6),
    track_name: str = Query(..., description="Название направления (например, ПИ, ФИТ, МОА)"),
    current_lecturer_id: int = Depends(get_current_lecturer_id),
    db: AsyncSession = Depends(get_db)
):
    """
    Получить статистику посещаемости за 4 недели для указанного курса и направления
    
    - **course_number**: Номер курса (1-6)
    - **track_name**: Название направления (например, ПИ, ФИТ, МОА)
    
    Возвращает данные по неделям с указанием четности/нечетности недели
    """
    try:
        weeks = await get_four_weeks_attendance_stats(
            db, 
            course_number=course_number, 
            track_name=track_name
        )
        
        if not weeks:
            return format_response(
                data={"weeks": []},
                message=f"No groups found for course {course_number} and direction {track_name}",
                code=200
            )
        
        return format_response(
            data={"weeks": weeks},
            message=f"Four weeks attendance statistics retrieved successfully for course {course_number}, direction {track_name}",
            code=200
        )
        
    except Exception as e:
        return format_response(
            message=str(e),
            code=400
        )

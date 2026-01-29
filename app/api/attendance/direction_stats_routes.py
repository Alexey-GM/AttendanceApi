from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.session import get_db
from app.schemas.attendance import DirectionAttendanceResponse
from app.services.direction_stats_service import get_direction_attendance_stats
from app.utils.jwt import get_current_lecturer_id
from app.utils.response import format_response

router = APIRouter(prefix="/direction-stats", tags=["direction-stats"])

@router.get("/attendance", response_model=DirectionAttendanceResponse)
async def get_direction_attendance_statistics(
    current_lecturer_id: int = Depends(get_current_lecturer_id),
    db: AsyncSession = Depends(get_db)
):
    """
    Получить статистику посещаемости по направлениям для разных периодов
    """
    try:
        stats = await get_direction_attendance_stats(db)
        
        return format_response(
            data={"periods": stats},
            message="Direction attendance statistics retrieved successfully",
            code=200
        )
        
    except Exception as e:
        return format_response(
            message=str(e),
            code=400
        )





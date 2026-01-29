from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.session import get_db
from app.schemas.attendance import CourseAttendanceResponse
from app.services.attendance_stats_service import get_course_attendance_stats
from app.utils.jwt import get_current_lecturer_id
from app.utils.response import format_response

router = APIRouter(prefix="/course-stats", tags=["course-stats"])

@router.get("/attendance", response_model=CourseAttendanceResponse)
async def get_course_attendance_statistics(
    current_lecturer_id: int = Depends(get_current_lecturer_id),
    db: AsyncSession = Depends(get_db)
):
    """
    Получить статистику посещаемости по курсам для разных периодов
    """
    try:
        stats = await get_course_attendance_stats(db)
        
        return format_response(
            data={"periods": stats},
            message="Course attendance statistics retrieved successfully",
            code=200
        )
        
    except Exception as e:
        return format_response(
            message=str(e),
            code=400
        )





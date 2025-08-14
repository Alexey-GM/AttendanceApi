from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.session import get_db
from app.schemas.attendance import StudentAttendanceResponse
from app.services.student_attendance_service import get_student_attendance_stats
from app.utils.jwt import get_current_lecturer_id
from app.utils.response import format_response

router = APIRouter(prefix="/student-attendance", tags=["student-attendance"])

@router.get("/", response_model=StudentAttendanceResponse)
async def get_student_attendance_statistics(
    course_number: int = Query(..., description="Номер курса", ge=1, le=6),
    track_name: str = Query(..., description="Название направления (например, ПИ, ФИТ, МОА)"),
    current_lecturer_id: int = Depends(get_current_lecturer_id),
    db: AsyncSession = Depends(get_db)
):
    """
    Получить статистику посещаемости студентов за 4 недели для указанного курса и направления
    
    - **course_number**: Номер курса (1-6)
    - **track_name**: Название направления (например, ПИ, ФИТ, МОА)
    
    Возвращает данные о посещаемости каждого студента по дисциплинам и неделям
    """
    try:
        students_data = await get_student_attendance_stats(
            db, 
            course_number=course_number, 
            track_name=track_name
        )
        
        if not students_data:
            return format_response(
                data={"data": []},
                message=f"No students found for course {course_number} and direction {track_name}",
                code=200
            )
        
        return format_response(
            data={"data": students_data},
            message=f"Student attendance statistics retrieved successfully for course {course_number}, direction {track_name}. Found {len(students_data)} records.",
            code=200
        )
        
    except Exception as e:
        return format_response(
            message=str(e),
            code=400
        )

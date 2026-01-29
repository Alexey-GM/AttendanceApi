from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import date

from app.db.session import get_db
from app.schemas.attendance import GeneralStudentAttendanceResponse
from app.services.general_student_attendance_service import get_general_student_attendance
from app.utils.jwt import get_current_lecturer_id
from app.utils.response import format_response

router = APIRouter(prefix="/general-attendance", tags=["general-attendance"])

@router.get("/", response_model=GeneralStudentAttendanceResponse)
async def get_general_student_attendance_list(
    course_number: Optional[int] = Query(None, description="Номер курса", ge=1, le=6),
    track_name: Optional[str] = Query(None, description="Название направления (например, ПИ, ФИТ, МОА)"),
    student_id: Optional[int] = Query(None, description="ID конкретного студента"),
    start_date: Optional[str] = Query(None, description="Дата начала периода (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="Дата окончания периода (YYYY-MM-DD)"),
    limit: int = Query(default=100, description="Максимальное количество записей", ge=1, le=1000),
    current_lecturer_id: int = Depends(get_current_lecturer_id),
    db: AsyncSession = Depends(get_db)
):
    """
    Получить общую посещаемость студентов
    
    - **course_number**: Номер курса (1-6, опционально)
    - **track_name**: Название направления (например, ПИ, ФИТ, МОА, опционально)
    - **student_id**: ID конкретного студента (опционально)
    - **start_date**: Дата начала периода в формате YYYY-MM-DD (опционально)
    - **end_date**: Дата окончания периода в формате YYYY-MM-DD (опционально)
    - **limit**: Максимальное количество записей (по умолчанию 100, максимум 1000)
    
    Возвращает детальную информацию о посещаемости студентов
    """
    try:
        # Парсим даты если они переданы
        parsed_start_date = None
        parsed_end_date = None
        
        if start_date:
            try:
                parsed_start_date = date.fromisoformat(start_date)
            except ValueError:
                return format_response(
                    message="Invalid start_date format. Use YYYY-MM-DD",
                    code=400
                )
        
        if end_date:
            try:
                parsed_end_date = date.fromisoformat(end_date)
            except ValueError:
                return format_response(
                    message="Invalid end_date format. Use YYYY-MM-DD",
                    code=400
                )
        
        # Проверяем, что если переданы обе даты, то start_date <= end_date
        if parsed_start_date and parsed_end_date and parsed_start_date > parsed_end_date:
            return format_response(
                message="start_date cannot be later than end_date",
                code=400
            )
        
        attendance_records = await get_general_student_attendance(
            db,
            course_number=course_number,
            track_name=track_name,
            student_id=student_id,
            start_date=parsed_start_date,
            end_date=parsed_end_date,
            limit=limit
        )
        
        if not attendance_records:
            return format_response(
                data={"data": []},
                message="No attendance records found for the specified criteria",
                code=200
            )
        
        return format_response(
            data={"data": attendance_records},
            message=f"General student attendance retrieved successfully. Found {len(attendance_records)} records.",
            code=200
        )
        
    except Exception as e:
        return format_response(
            message=str(e),
            code=400
        )




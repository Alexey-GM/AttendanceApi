from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.session import get_db
from app.schemas.attendance import StudentsRiskResponse
from app.services.students_risk_service import get_students_at_risk
from app.utils.jwt import get_current_lecturer_id
from app.utils.response import format_response

router = APIRouter(prefix="/students-risk", tags=["students-risk"])

@router.get("/", response_model=StudentsRiskResponse)
async def get_students_at_risk_list(
    weeks_back: int = Query(default=2, description="Количество недель назад для анализа", ge=1, le=12),
    min_missed_sessions: int = Query(default=2, description="Минимальное количество занятий с пропусками", ge=1),
    min_missed_count: int = Query(default=2, description="Минимальное количество пропусков", ge=1),
    current_lecturer_id: int = Depends(get_current_lecturer_id),
    db: AsyncSession = Depends(get_db)
):
    """
    Получить список студентов в зоне риска
    
    - **weeks_back**: Количество недель назад для анализа (по умолчанию 2)
    - **min_missed_sessions**: Минимальное количество занятий с пропусками (по умолчанию 2)
    - **min_missed_count**: Минимальное количество пропусков (по умолчанию 2)
    """
    try:
        students = await get_students_at_risk(
            db, 
            weeks_back=weeks_back, 
            min_missed_sessions=min_missed_sessions, 
            min_missed_count=min_missed_count
        )
        
        return format_response(
            data={"students": students},
            message=f"Students at risk retrieved successfully. Found {len(students)} students.",
            code=200
        )
        
    except Exception as e:
        return format_response(
            message=str(e),
            code=400
        )






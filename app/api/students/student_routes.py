from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, join
from typing import List

from app.db.session import get_db
from app.models.student import Student
from app.models.group_enrollment import GroupEnrollment
from app.models.work_group import WorkGroup
from app.schemas.student import StudentResponse
from app.utils.jwt import get_current_lecturer_id
from app.utils.response import format_response

router = APIRouter(prefix="/students", tags=["students"])

@router.get("/work-group/{work_group_id}", response_model=List[StudentResponse])
async def get_students_by_work_group(
    work_group_id: int,
    current_lecturer_id: int = Depends(get_current_lecturer_id),
    db: AsyncSession = Depends(get_db)
):
    """
    Получить список студентов для указанной рабочей группы
    """
    try:
        # Проверяем существование work_group
        work_group_query = select(WorkGroup).where(WorkGroup.id == work_group_id)
        work_group_result = await db.execute(work_group_query)
        work_group = work_group_result.scalar_one_or_none()
        
        if not work_group:
            return format_response(
                message="Work group not found",
                code=404
            )
        
        # Получаем студентов через связь group_enrollment
        query = (
            select(Student)
            .join(GroupEnrollment, Student.id == GroupEnrollment.student_id)
            .where(
                GroupEnrollment.work_group_id == work_group_id,
                GroupEnrollment.is_active == True
            )
        )
        
        result = await db.execute(query)
        students = result.scalars().all()
        
        # Преобразуем студентов в словари для избежания проблем с сериализацией
        students_data = []
        for student in students:
            student_dict = {
                "id": student.id,
                "first_name": student.first_name,
                "last_name": student.last_name,
                "middle_name": student.middle_name,
                "date_birth": student.date_birth.isoformat() if student.date_birth else None,
                "base_group_id": student.base_group_id
            }
            students_data.append(student_dict)
        
        return format_response(
            data=students_data,
            message="Students retrieved successfully",
            code=200
        )
        
    except Exception as e:
        return format_response(
            message=f"Error retrieving students: {str(e)}",
            code=400
        ) 
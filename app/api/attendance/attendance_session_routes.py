from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.db.session import get_db
from app.models.attendance_session import AttendanceSession
from app.models.attendance import Attendance
from app.models.student import Student
from app.models.attendance_status import AttendanceStatus
from app.models.classroom import Classroom
from app.models.discipline_plan import DisciplinePlan
from app.schemas.attendance import AttendanceSessionResponse, CreateAttendanceSessionRequest
from app.utils.jwt import get_current_lecturer_id
from app.utils.response import format_response

router = APIRouter(prefix="/attendance-sessions", tags=["attendance-sessions"])

@router.get("/discipline-plan/{discipline_plan_id}")
async def get_attendance_sessions_by_discipline_plan(
    discipline_plan_id: int,
    current_lecturer_id: int = Depends(get_current_lecturer_id),
    db: AsyncSession = Depends(get_db)
):
    """
    Получить все attendance sessions для указанного discipline_plan_id
    """
    try:
        # Проверяем существование discipline_plan
        discipline_plan_query = select(DisciplinePlan).where(DisciplinePlan.id == discipline_plan_id)
        discipline_plan_result = await db.execute(discipline_plan_query)
        discipline_plan = discipline_plan_result.scalar_one_or_none()
        
        if not discipline_plan:
            return format_response(
                message="Discipline plan not found",
                code=404
            )
        
        # Получаем все attendance sessions для данного discipline_plan
        sessions_query = select(AttendanceSession).where(
            AttendanceSession.discipline_plan_id == discipline_plan_id
        )
        sessions_result = await db.execute(sessions_query)
        sessions = sessions_result.scalars().all()
        
        # Подготавливаем данные для ответа
        sessions_data = []
        
        for session in sessions:
            # Получаем classroom для session
            classroom_query = select(Classroom).where(Classroom.id == session.classroom_id)
            classroom_result = await db.execute(classroom_query)
            classroom = classroom_result.scalar_one_or_none()
            
            # Получаем все attendances для данной session
            attendances_query = select(Attendance).where(
                Attendance.attendance_session_id == session.id
            )
            attendances_result = await db.execute(attendances_query)
            attendances = attendances_result.scalars().all()
            
            # Подготавливаем данные attendances
            attendances_data = []
            
            for attendance in attendances:
                # Получаем студента
                student_query = select(Student).where(Student.id == attendance.student_id)
                student_result = await db.execute(student_query)
                student = student_result.scalar_one_or_none()
                
                # Получаем attendance status
                status_query = select(AttendanceStatus).where(AttendanceStatus.id == attendance.attendance_status_id)
                status_result = await db.execute(status_query)
                status = status_result.scalar_one_or_none()
                
                if student and status:
                    attendance_dict = {
                        "id": attendance.id,
                        "student": {
                            "id": student.id,
                            "first_name": student.first_name,
                            "last_name": student.last_name,
                            "middle_name": student.middle_name,
                            "date_birth": student.date_birth.isoformat() if student.date_birth else None,
                            "base_group_id": student.base_group_id
                        },
                        "attendance_status": {
                            "id": status.id,
                            "name": status.name,
                            "comment": status.comment
                        },
                        "attendance_timestamp": attendance.attendance_timestamp.isoformat() if attendance.attendance_timestamp else None,
                        "comment": attendance.comment
                    }
                    attendances_data.append(attendance_dict)
            
            # Формируем данные session
            session_dict = {
                "id": session.id,
                "date": session.date.isoformat() if session.date else None,
                "classroom": {
                    "id": classroom.id,
                    "name": classroom.name
                } if classroom else None,
                "attendances": attendances_data
            }
            
            sessions_data.append(session_dict)
        
        return format_response(
            data=sessions_data,
            message="Attendance sessions retrieved successfully",
            code=200
        )
        
    except Exception as e:
        return format_response(
            message=f"Error retrieving attendance sessions: {str(e)}",
            code=400
        )

@router.post("/")
async def create_attendance_session(
    request: CreateAttendanceSessionRequest,
    current_lecturer_id: int = Depends(get_current_lecturer_id),
    db: AsyncSession = Depends(get_db)
):
    """
    Создать новую attendance session
    """
    try:
        # Проверяем существование discipline_plan
        discipline_plan_query = select(DisciplinePlan).where(DisciplinePlan.id == request.discipline_plan_id)
        discipline_plan_result = await db.execute(discipline_plan_query)
        discipline_plan = discipline_plan_result.scalar_one_or_none()
        
        if not discipline_plan:
            return format_response(
                message="Discipline plan not found",
                code=404
            )
        
        # Проверяем существование classroom
        classroom_query = select(Classroom).where(Classroom.id == request.classroom_id)
        classroom_result = await db.execute(classroom_query)
        classroom = classroom_result.scalar_one_or_none()
        
        if not classroom:
            return format_response(
                message="Classroom not found",
                code=404
            )
        
        # Проверяем, что преподаватель имеет доступ к данному discipline_plan
        if discipline_plan.lecturer_id != current_lecturer_id:
            return format_response(
                message="Access denied: you can only create sessions for your own discipline plans",
                code=403
            )
        
        # Создаем новую attendance session
        new_session = AttendanceSession(
            discipline_plan_id=request.discipline_plan_id,
            date=request.date,
            classroom_id=request.classroom_id
        )
        
        db.add(new_session)
        await db.commit()
        await db.refresh(new_session)
        
        # Получаем данные classroom для ответа
        classroom_data = {
            "id": classroom.id,
            "name": classroom.name
        }
        
        # Формируем ответ
        session_data = {
            "id": new_session.id,
            "date": new_session.date.isoformat() if new_session.date else None,
            "classroom": classroom_data,
            "attendances": []
        }
        
        return format_response(
            data=session_data,
            message="Attendance session created successfully",
            code=201
        )
        
    except Exception as e:
        await db.rollback()
        return format_response(
            message=f"Error creating attendance session: {str(e)}",
            code=400
        ) 
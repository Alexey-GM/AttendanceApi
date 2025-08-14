from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, case
from sqlalchemy.orm import joinedload
from datetime import datetime, timedelta, date
from typing import List, Dict, Any, Optional
from app.models.base_group import BaseGroup
from app.models.student import Student
from app.models.attendance import Attendance
from app.models.attendance_session import AttendanceSession
from app.models.attendance_status import AttendanceStatus
from app.models.discipline_plan import DisciplinePlan
from app.models.track import Track
from app.models.discipline import Discipline
from app.models.lecturer import Lecturer

async def get_general_student_attendance(
    db: AsyncSession,
    course_number: Optional[int] = None,
    track_name: Optional[str] = None,
    student_id: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    limit: int = 100
) -> List[Dict[str, Any]]:
    """
    Получить общую посещаемость студентов
    
    Args:
        db: Сессия базы данных
        course_number: Номер курса (опционально)
        track_name: Название направления (опционально)
        student_id: ID конкретного студента (опционально)
        start_date: Дата начала периода (опционально)
        end_date: Дата окончания периода (опционально)
        limit: Максимальное количество записей (по умолчанию 100)
    
    Returns:
        Список записей о посещаемости студентов
    """
    try:
        # Базовый запрос для получения данных о посещаемости
        base_query = select(
            Student.id.label('student_id'),
            Student.first_name,
            Student.last_name,
            Student.middle_name,
            BaseGroup.name.label('group_name'),
            BaseGroup.course_number,
            Track.name.label('track_name'),
            Discipline.name.label('discipline_name'),
            Lecturer.first_name.label('lecturer_first_name'),
            Lecturer.last_name.label('lecturer_last_name'),
            Lecturer.middle_name.label('lecturer_middle_name'),
            AttendanceSession.date,
            AttendanceStatus.id.label('status_id'),
            AttendanceStatus.name.label('status_name'),
            Attendance.comment
        ).join(
            BaseGroup, Student.base_group_id == BaseGroup.id
        ).join(
            Track, BaseGroup.track_id == Track.id
        ).join(
            Attendance, Student.id == Attendance.student_id
        ).join(
            AttendanceSession, Attendance.attendance_session_id == AttendanceSession.id
        ).join(
            DisciplinePlan, AttendanceSession.discipline_plan_id == DisciplinePlan.id
        ).join(
            Discipline, DisciplinePlan.discipline_id == Discipline.id
        ).join(
            Lecturer, DisciplinePlan.lecturer_id == Lecturer.id
        ).join(
            AttendanceStatus, Attendance.attendance_status_id == AttendanceStatus.id
        )
        
        # Применяем фильтры
        where_conditions = []
        
        if course_number is not None:
            where_conditions.append(BaseGroup.course_number == course_number)
        
        if track_name is not None:
            where_conditions.append(Track.name == track_name)
        
        if student_id is not None:
            where_conditions.append(Student.id == student_id)
        
        if start_date is not None:
            where_conditions.append(AttendanceSession.date >= start_date)
        
        if end_date is not None:
            where_conditions.append(AttendanceSession.date <= end_date)
        
        if where_conditions:
            base_query = base_query.where(and_(*where_conditions))
        
        # Добавляем сортировку и лимит
        base_query = base_query.order_by(
            AttendanceSession.date.desc(),
            Student.last_name,
            Student.first_name
        ).limit(limit)
        
        # Выполняем запрос
        result = await db.execute(base_query)
        records = result.fetchall()
        
        # Формируем результат
        attendance_records = []
        
        for record in records:
            # Формируем ФИО студента
            first_initial = record.first_name[0] + "." if record.first_name else ""
            middle_initial = record.middle_name[0] + "." if record.middle_name else ""
            last_initial = record.last_name[0] + "." if record.last_name else ""
            
            full_name = f"{record.last_name} {first_initial}{middle_initial}"
            
            # Формируем название группы
            group_name = f"{record.track_name}-{record.group_name}"
            
            # Формируем ФИО преподавателя
            lecturer_first_initial = record.lecturer_first_name[0] + "." if record.lecturer_first_name else ""
            lecturer_middle_initial = record.lecturer_middle_name[0] + "." if record.lecturer_middle_name else ""
            lecturer_last_initial = record.lecturer_last_name[0] + "." if record.lecturer_last_name else ""
            
            teacher_name = f"{record.lecturer_last_name} {lecturer_first_initial}{lecturer_middle_initial}"
            
            # Определяем статус (1 - присутствовал, 0 - отсутствовал)
            # Ищем ключевые слова в названии статуса
            status_value = 0  # По умолчанию отсутствовал
            if record.status_name:
                if any(keyword in record.status_name.lower() for keyword in ['присутствовал', 'явился', 'был']):
                    status_value = 1
            
            # Форматируем комментарий
            comment = record.comment if record.comment else "—"
            
            # Форматируем дату в ISO формате
            date_iso = record.date.isoformat() + "Z" if record.date else ""
            
            attendance_records.append({
                "fullName": full_name,
                "group": group_name,
                "course": record.course_number,
                "subject": record.discipline_name,
                "teacher": teacher_name,
                "date": date_iso,
                "status": status_value,
                "comment": comment
            })
        
        return attendance_records
        
    except Exception as e:
        raise Exception(f"Error getting general student attendance: {str(e)}")

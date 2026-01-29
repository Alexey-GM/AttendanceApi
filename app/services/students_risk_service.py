from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, case
from sqlalchemy.orm import joinedload
from datetime import datetime, timedelta, date
from typing import List, Dict
from app.models.base_group import BaseGroup
from app.models.student import Student
from app.models.attendance import Attendance
from app.models.attendance_session import AttendanceSession
from app.models.attendance_status import AttendanceStatus
from app.models.discipline_plan import DisciplinePlan
from app.models.track import Track

async def get_students_at_risk(db: AsyncSession, weeks_back: int = 2, min_missed_sessions: int = 2, min_missed_count: int = 2) -> List[Dict[str, any]]:
    """
    Получить список студентов в зоне риска
    
    Args:
        db: Сессия базы данных
        weeks_back: Количество недель назад для анализа (по умолчанию 2)
        min_missed_sessions: Минимальное количество занятий с пропусками (по умолчанию 2)
        min_missed_count: Минимальное количество пропусков (по умолчанию 2)
    """
    try:
        # Определяем период анализа
        today = date.today()
        start_date = today - timedelta(weeks=weeks_back)
        
        # Получаем студентов с количеством пропусков
        # Считаем только записи, где статус посещения указывает на пропуск
        # Предполагаем, что статус с id=2 (или другим) означает "пропустил"
        
        # Сначала получаем все статусы посещения
        statuses_query = select(AttendanceStatus.id, AttendanceStatus.name)
        statuses_result = await db.execute(statuses_query)
        statuses = {row[1]: row[0] for row in statuses_result.fetchall()}
        
        # Определяем ID статуса для пропусков (обычно это "Пропустил", "Отсутствовал" и т.д.)
        # Если точный статус не найден, используем все статусы кроме "Присутствовал"
        missed_status_ids = []
        present_status_id = None
        
        for status_name, status_id in statuses.items():
            if any(keyword in status_name.lower() for keyword in ['пропустил', 'отсутствовал', 'не явился', 'болел']):
                missed_status_ids.append(status_id)
            elif any(keyword in status_name.lower() for keyword in ['присутствовал', 'явился', 'был']):
                present_status_id = status_id
        
        # Если не нашли статусы пропусков, используем все кроме присутствия
        if not missed_status_ids and present_status_id:
            missed_status_ids = [status_id for status_id in statuses.values() if status_id != present_status_id]
        
        # Если все еще нет, используем все статусы
        if not missed_status_ids:
            missed_status_ids = list(statuses.values())
        
        # Получаем студентов с количеством пропусков
        students_risk_query = select(
            Student.id,
            Student.first_name,
            Student.last_name,
            Student.middle_name,
            BaseGroup.name.label('group_name'),
            Track.name.label('track_name'),
            func.count(Attendance.id).label('total_missed')
        ).join(
            BaseGroup, Student.base_group_id == BaseGroup.id
        ).join(
            Track, BaseGroup.track_id == Track.id
        ).join(
            Attendance, Student.id == Attendance.student_id
        ).join(
            AttendanceSession, Attendance.attendance_session_id == AttendanceSession.id
        ).where(
            and_(
                Attendance.attendance_status_id.in_(missed_status_ids),
                AttendanceSession.date >= start_date,
                AttendanceSession.date <= today
            )
        ).group_by(
            Student.id,
            Student.first_name,
            Student.last_name,
            Student.middle_name,
            BaseGroup.name,
            Track.name
        ).having(
            func.count(Attendance.id) >= min_missed_count
        )
        
        students_result = await db.execute(students_risk_query)
        students_data = students_result.fetchall()
        
        # Формируем результат
        result = []
        for student in students_data:
            # Формируем ФИО в формате "Фамилия И.О."
            first_initial = student.first_name[0] + "." if student.first_name else ""
            middle_initial = student.middle_name[0] + "." if student.middle_name else ""
            last_initial = student.last_name[0] + "." if student.last_name else ""
            
            full_name = f"{student.last_name} {first_initial}{middle_initial}"
            
            # Формируем название группы в формате "Трек-Группа"
            group_name = f"{student.track_name}-{student.group_name}"
            
            result.append({
                "name": full_name,
                "group": group_name,
                "missed": student.total_missed
            })
        
        # Сортируем по количеству пропусков (по убыванию)
        result.sort(key=lambda x: x["missed"], reverse=True)
        
        return result
        
    except Exception as e:
        raise Exception(f"Error calculating students at risk: {str(e)}")






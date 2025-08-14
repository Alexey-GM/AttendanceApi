from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, case
from sqlalchemy.orm import joinedload
from datetime import datetime, timedelta, date
from typing import List, Dict, Any
from app.models.base_group import BaseGroup
from app.models.student import Student
from app.models.attendance import Attendance
from app.models.attendance_session import AttendanceSession
from app.models.attendance_status import AttendanceStatus
from app.models.discipline_plan import DisciplinePlan
from app.models.track import Track

def get_iso_week_number(target_date: date, academic_year_start: date = None) -> int:
    """
    Вычисляет номер недели от начала учебного года
    
    Args:
        target_date: Дата для которой нужно вычислить номер недели
        academic_year_start: Дата начала учебного года (по умолчанию 1 сентября текущего года)
    
    Returns:
        Номер недели от начала учебного года
    """
    if academic_year_start is None:
        # По умолчанию начало учебного года - 1 сентября текущего года
        current_year = target_date.year
        if target_date.month < 9:  # Если текущий месяц до сентября
            academic_year_start = date(current_year - 1, 9, 1)
        else:
            academic_year_start = date(current_year, 9, 1)
    
    # Вычисляем количество дней от начала учебного года
    days_diff = (target_date - academic_year_start).days
    
    # Вычисляем номер недели (начиная с 1)
    week_number = (days_diff // 7) + 1
    
    return max(1, week_number)

def is_even_week(week_number: int) -> bool:
    """
    Определяет, является ли неделя четной
    
    Args:
        week_number: Номер недели
    
    Returns:
        True если неделя четная, False если нечетная
    """
    return week_number % 2 == 0

async def get_four_weeks_attendance_stats(
    db: AsyncSession, 
    course_number: int, 
    track_name: str
) -> List[Dict[str, Any]]:
    """
    Получить статистику посещаемости за 4 недели для указанного курса и направления
    
    Args:
        db: Сессия базы данных
        course_number: Номер курса
        track_name: Название направления (например, "ПИ", "ФИТ", "МОА")
    
    Returns:
        Список недель с данными о посещаемости
    """
    try:
        # Получаем все группы для указанного курса и направления
        groups_query = select(
            BaseGroup.id,
            BaseGroup.name,
            BaseGroup.course_number,
            Track.name.label('track_name')
        ).join(
            Track, BaseGroup.track_id == Track.id
        ).where(
            and_(
                BaseGroup.course_number == course_number,
                Track.name == track_name
            )
        )
        
        groups_result = await db.execute(groups_query)
        groups = groups_result.fetchall()
        
        if not groups:
            return []
        
        # Определяем период анализа - последние 4 недели
        today = date.today()
        
        # Получаем все статусы посещения
        statuses_query = select(AttendanceStatus.id, AttendanceStatus.name)
        statuses_result = await db.execute(statuses_query)
        statuses = {row[1]: row[0] for row in statuses_result.fetchall()}
        
        # Определяем ID статуса для присутствия
        present_status_id = None
        for status_name, status_id in statuses.items():
            if any(keyword in status_name.lower() for keyword in ['присутствовал', 'явился', 'был']):
                present_status_id = status_id
                break
        
        # Если не нашли статус присутствия, используем первый
        if not present_status_id and statuses:
            present_status_id = list(statuses.values())[0]
        
        result = []
        
        # Генерируем 4 недели
        for week_offset in range(4):
            week_start = today - timedelta(weeks=week_offset + 1)
            week_end = week_start + timedelta(days=6)
            
            # Вычисляем номер недели от начала учебного года
            iso_week = get_iso_week_number(week_start)
            even = is_even_week(iso_week)
            
            week_data = []
            
            # Для каждой группы получаем статистику посещаемости за неделю
            for group in groups:
                group_full_name = f"{group.track_name}-{group.name}"
                
                # Получаем количество студентов в группе
                students_count_query = select(func.count(Student.id)).where(
                    Student.base_group_id == group.id
                )
                students_count_result = await db.execute(students_count_query)
                total_students = students_count_result.scalar() or 0
                
                if total_students == 0:
                    continue
                
                # Получаем количество занятий для группы за эту неделю
                sessions_count_query = select(func.count(AttendanceSession.id)).join(
                    DisciplinePlan, AttendanceSession.discipline_plan_id == DisciplinePlan.id
                ).where(
                    and_(
                        DisciplinePlan.work_group_id == group.id,
                        AttendanceSession.date >= week_start,
                        AttendanceSession.date <= week_end
                    )
                )
                
                sessions_count_result = await db.execute(sessions_count_query)
                total_sessions = sessions_count_result.scalar() or 0
                
                if total_sessions == 0:
                    continue
                
                # Получаем количество присутствующих студентов за неделю
                present_count_query = select(func.count(Attendance.id)).join(
                    Student, Attendance.student_id == Student.id
                ).join(
                    AttendanceSession, Attendance.attendance_session_id == AttendanceSession.id
                ).join(
                    DisciplinePlan, AttendanceSession.discipline_plan_id == DisciplinePlan.id
                ).where(
                    and_(
                        Student.base_group_id == group.id,
                        Attendance.attendance_status_id == present_status_id,
                        AttendanceSession.date >= week_start,
                        AttendanceSession.date <= week_end
                    )
                )
                
                present_count_result = await db.execute(present_count_query)
                present_students = present_count_result.scalar() or 0
                
                # Вычисляем процент посещаемости за неделю
                expected_attendances = total_students * total_sessions
                if expected_attendances > 0:
                    attendance_percentage = min(100.0, (present_students / expected_attendances) * 100)
                else:
                    attendance_percentage = 0.0
                
                week_data.append({
                    "group": group_full_name,
                    "direction": group.track_name,
                    "course": str(group.course_number),
                    "attendancePercent": round(attendance_percentage, 1)
                })
            
            # Добавляем неделю в результат только если есть данные
            if week_data:
                result.append({
                    "weekStart": week_start.strftime('%Y-%m-%d'),
                    "weekEnd": week_end.strftime('%Y-%m-%d'),
                    "isoWeek": iso_week,
                    "even": even,
                    "data": week_data
                })
            else:
                # Добавляем пустую неделю если нет данных
                result.append({
                    "weekStart": week_start.strftime('%Y-%m-%d'),
                    "weekEnd": week_end.strftime('%Y-%m-%d'),
                    "isoWeek": iso_week,
                    "even": even,
                    "data": []
                })
        
        # Сортируем недели по убыванию (последние недели первыми)
        result.sort(key=lambda x: x["isoWeek"], reverse=True)
        
        return result
        
    except Exception as e:
        raise Exception(f"Error calculating four weeks attendance stats: {str(e)}")

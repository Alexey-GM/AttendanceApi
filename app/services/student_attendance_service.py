from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, case, distinct
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
from app.models.discipline import Discipline
from app.models.activity_type import ActivityType

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

def get_week_type(even: bool) -> str:
    """
    Возвращает тип недели на русском языке
    
    Args:
        even: True если неделя четная
    
    Returns:
        "Чет" или "Нечет"
    """
    return "Чет" if even else "Нечет"

async def get_student_attendance_stats(
    db: AsyncSession, 
    course_number: int, 
    track_name: str
) -> List[Dict[str, Any]]:
    """
    Получить статистику посещаемости студентов за 4 недели для указанного курса и направления
    
    Args:
        db: Сессия базы данных
        course_number: Номер курса
        track_name: Название направления (например, "ПИ", "ФИТ", "МОА")
    
    Returns:
        Список студентов с данными о посещаемости по дисциплинам и неделям
    """
    try:
        # Получаем всех студентов для указанного курса и направления
        students_query = select(
            Student.id,
            Student.first_name,
            Student.last_name,
            Student.middle_name,
            BaseGroup.course_number,
            Track.name.label('track_name')
        ).join(
            BaseGroup, Student.base_group_id == BaseGroup.id
        ).join(
            Track, BaseGroup.track_id == Track.id
        ).where(
            and_(
                BaseGroup.course_number == course_number,
                Track.name == track_name
            )
        )
        
        students_result = await db.execute(students_query)
        students = students_result.fetchall()
        
        if not students:
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
        
        # Для каждого студента получаем данные о посещаемости
        for student in students:
            # Формируем ФИО студента
            first_initial = student.first_name[0] + "." if student.first_name else ""
            middle_initial = student.middle_name[0] + "." if student.middle_name else ""
            last_initial = student.last_name[0] + "." if student.last_name else ""
            
            full_name = f"{student.last_name} {first_initial}{middle_initial}"
            
            # Получаем уникальные дисциплины и типы занятий для студента
            disciplines_query = select(
                Discipline.name.label('discipline_name'),
                ActivityType.name.label('activity_type_name')
            ).join(
                DisciplinePlan, Discipline.id == DisciplinePlan.discipline_id
            ).join(
                ActivityType, DisciplinePlan.activity_type_id == ActivityType.id
            ).join(
                AttendanceSession, DisciplinePlan.id == AttendanceSession.discipline_plan_id
            ).join(
                Attendance, AttendanceSession.id == Attendance.attendance_session_id
            ).where(
                Attendance.student_id == student.id
            ).distinct()
            
            disciplines_result = await db.execute(disciplines_query)
            disciplines = disciplines_result.fetchall()
            
            # Для каждой дисциплины и типа занятия создаем запись
            for discipline in disciplines:
                discipline_name = discipline.discipline_name
                activity_type_name = discipline.activity_type_name
                
                # Определяем общий период (4 недели)
                period_start = today - timedelta(weeks=4)
                period_end = today
                
                weeks_data = []
                
                # Генерируем 4 недели
                for week_offset in range(4):
                    week_start = today - timedelta(weeks=week_offset + 1)
                    week_end = week_start + timedelta(days=6)
                    
                    # Вычисляем номер недели от начала учебного года
                    iso_week = get_iso_week_number(week_start)
                    even = is_even_week(iso_week)
                    week_type = get_week_type(even)
                    
                    # Получаем количество занятий по данной дисциплине и типу для студента за неделю
                    sessions_count_query = select(func.count(AttendanceSession.id)).join(
                        DisciplinePlan, AttendanceSession.discipline_plan_id == DisciplinePlan.id
                    ).join(
                        Discipline, DisciplinePlan.discipline_id == Discipline.id
                    ).join(
                        ActivityType, DisciplinePlan.activity_type_id == ActivityType.id
                    ).where(
                        and_(
                            Discipline.name == discipline_name,
                            ActivityType.name == activity_type_name,
                            AttendanceSession.date >= week_start,
                            AttendanceSession.date <= week_end
                        )
                    )
                    
                    sessions_count_result = await db.execute(sessions_count_query)
                    total_sessions = sessions_count_result.scalar() or 0
                    
                    if total_sessions == 0:
                        # Если нет занятий за неделю, добавляем неделю с 0% посещаемости
                        weeks_data.append({
                            "weekType": week_type,
                            "start": week_start.strftime('%Y-%m-%d'),
                            "end": week_end.strftime('%Y-%m-%d'),
                            "isoWeek": iso_week,
                            "attendancePercent": 0.0
                        })
                        continue
                    
                    # Получаем количество присутствий студента по данной дисциплине и типу за неделю
                    present_count_query = select(func.count(Attendance.id)).join(
                        AttendanceSession, Attendance.attendance_session_id == AttendanceSession.id
                    ).join(
                        DisciplinePlan, AttendanceSession.discipline_plan_id == DisciplinePlan.id
                    ).join(
                        Discipline, DisciplinePlan.discipline_id == Discipline.id
                    ).join(
                        ActivityType, DisciplinePlan.activity_type_id == ActivityType.id
                    ).where(
                        and_(
                            Attendance.student_id == student.id,
                            Discipline.name == discipline_name,
                            ActivityType.name == activity_type_name,
                            Attendance.attendance_status_id == present_status_id,
                            AttendanceSession.date >= week_start,
                            AttendanceSession.date <= week_end
                        )
                    )
                    
                    present_count_result = await db.execute(present_count_query)
                    present_sessions = present_count_result.scalar() or 0
                    
                    # Вычисляем процент посещаемости за неделю
                    if total_sessions > 0:
                        attendance_percentage = min(100.0, (present_sessions / total_sessions) * 100)
                    else:
                        attendance_percentage = 0.0
                    
                    weeks_data.append({
                        "weekType": week_type,
                        "start": week_start.strftime('%Y-%m-%d'),
                        "end": week_end.strftime('%Y-%m-%d'),
                        "isoWeek": iso_week,
                        "attendancePercent": round(attendance_percentage, 0)
                    })
                
                # Сортируем недели по убыванию (последние недели первыми)
                weeks_data.sort(key=lambda x: x["isoWeek"], reverse=True)
                
                # Добавляем данные студента
                result.append({
                    "student": full_name,
                    "subject": discipline_name,
                    "lessonType": activity_type_name,
                    "period": {
                        "startDate": period_start.strftime('%Y-%m-%d'),
                        "endDate": period_end.strftime('%Y-%m-%d')
                    },
                    "weeks": weeks_data
                })
        
        return result
        
    except Exception as e:
        raise Exception(f"Error calculating student attendance stats: {str(e)}")

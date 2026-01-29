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

async def get_group_attendance_stats(
    db: AsyncSession, 
    course_number: int, 
    track_name: str,
    weeks_count: int = 4
) -> List[Dict[str, Any]]:
    """
    Получить статистику посещаемости по группам для указанного курса и направления
    
    Args:
        db: Сессия базы данных
        course_number: Номер курса
        track_name: Название направления (например, "ПИ", "ФИТ", "МОА")
        weeks_count: Количество недель для анализа (по умолчанию 4)
    """
    try:
        # Получаем все группы для указанного курса и направления
        groups_query = select(
            BaseGroup.id,
            BaseGroup.name,
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
        
        # Определяем период анализа
        today = date.today()
        start_date = today - timedelta(weeks=weeks_count)
        
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
        
        # Генерируем недели
        for week_offset in range(weeks_count):
            week_start = today - timedelta(weeks=week_offset + 1)
            week_end = week_start + timedelta(days=6)
            
            # Форматируем название недели
            week_name = f"{week_start.strftime('%d.%m.%Y')} – {week_end.strftime('%d.%m.%Y')}"
            
            week_data = []
            daily_stats = {}
            
            # Получаем данные по дням недели
            for day_offset in range(7):
                current_date = week_start + timedelta(days=day_offset)
                
                if current_date > today:
                    continue
                
                day_data = {"date": current_date.strftime('%d.%m')}
                
                # Для каждой группы получаем статистику посещаемости
                for group in groups:
                    group_full_name = f"{group.track_name}-{group.name}"
                    
                    # Получаем количество студентов в группе
                    students_count_query = select(func.count(Student.id)).where(
                        Student.base_group_id == group.id
                    )
                    students_count_result = await db.execute(students_count_query)
                    total_students = students_count_result.scalar() or 0
                    
                    if total_students == 0:
                        day_data[group_full_name] = 0.0
                        continue
                    
                    # Получаем количество занятий для группы в этот день
                    sessions_count_query = select(func.count(AttendanceSession.id)).join(
                        DisciplinePlan, AttendanceSession.discipline_plan_id == DisciplinePlan.id
                    ).where(
                        and_(
                            DisciplinePlan.work_group_id == group.id,
                            AttendanceSession.date == current_date
                        )
                    )
                    
                    sessions_count_result = await db.execute(sessions_count_query)
                    total_sessions = sessions_count_result.scalar() or 0
                    
                    if total_sessions == 0:
                        day_data[group_full_name] = 0.0
                        continue
                    
                    # Получаем количество присутствующих студентов
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
                            AttendanceSession.date == current_date
                        )
                    )
                    
                    present_count_result = await db.execute(present_count_query)
                    present_students = present_count_result.scalar() or 0
                    
                    # Вычисляем процент посещаемости
                    expected_attendances = total_students * total_sessions
                    if expected_attendances > 0:
                        attendance_percentage = min(100.0, (present_students / expected_attendances) * 100)
                    else:
                        attendance_percentage = 0.0
                    
                    day_data[group_full_name] = round(attendance_percentage, 2)
                    
                    # Сохраняем статистику для вычисления тренда
                    if group_full_name not in daily_stats:
                        daily_stats[group_full_name] = []
                    daily_stats[group_full_name].append(attendance_percentage)
                
                week_data.append(day_data)
            
            # Вычисляем тренд для каждой группы
            trend = {}
            for group in groups:
                group_full_name = f"{group.track_name}-{group.name}"
                if group_full_name in daily_stats and len(daily_stats[group_full_name]) >= 2:
                    # Простой тренд: сравниваем среднее за последние 3 дня с предыдущими днями
                    recent_avg = sum(daily_stats[group_full_name][-3:]) / min(3, len(daily_stats[group_full_name][-3:]))
                    earlier_avg = sum(daily_stats[group_full_name][:-3]) / max(1, len(daily_stats[group_full_name][:-3]))
                    
                    if recent_avg > earlier_avg + 5:  # Порог в 5%
                        trend[group_full_name] = "up"
                    elif recent_avg < earlier_avg - 5:
                        trend[group_full_name] = "down"
                    else:
                        trend[group_full_name] = "stable"
                else:
                    trend[group_full_name] = "stable"
            
            result.append({
                "week": week_name,
                "data": week_data,
                "trend": trend
            })
        
        return result
        
    except Exception as e:
        raise Exception(f"Error calculating group attendance stats: {str(e)}")




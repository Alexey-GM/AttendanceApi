from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
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
from app.models.specialty import Specialty

async def get_direction_attendance_stats(db: AsyncSession) -> Dict[str, List[Dict[str, any]]]:
    """
    Получить статистику посещаемости по направлениям для разных периодов
    """
    try:
        # Получаем все направления с их сокращенными названиями
        # Используем track.name для получения сокращенных названий (например, "ПИ", "ФИТ")
        directions_query = select(Track.id, Track.name)
        directions_result = await db.execute(directions_query)
        directions = [(row[0], row[1]) for row in directions_result.fetchall()]
        
        # Определяем периоды
        today = date.today()
        periods = {
            "Прошлая неделя": today - timedelta(days=7),
            "Прошлый месяц": today - timedelta(days=30),
            "Прошлый семестр": today - timedelta(days=90)
        }
        
        result = {}
        
        for period_name, start_date in periods.items():
            period_stats = []
            
            for track_id, direction_name in directions:
                # Получаем количество студентов на данном направлении
                students_count_query = select(func.count(Student.id)).join(
                    BaseGroup, Student.base_group_id == BaseGroup.id
                ).where(BaseGroup.track_id == track_id)
                
                students_count_result = await db.execute(students_count_query)
                total_students = students_count_result.scalar()
                
                if total_students == 0:
                    period_stats.append({
                        "direction": direction_name,
                        "attendance": 0.0
                    })
                    continue
                
                # Получаем количество занятий для данного направления в указанный период
                # Сначала получаем все группы на данном направлении
                groups_query = select(BaseGroup.id).where(BaseGroup.track_id == track_id)
                groups_result = await db.execute(groups_query)
                group_ids = [row[0] for row in groups_result.fetchall()]
                
                if not group_ids:
                    period_stats.append({
                        "direction": direction_name,
                        "attendance": 0.0
                    })
                    continue
                
                # Получаем количество занятий для групп данного направления в указанный период
                sessions_count_query = select(func.count(AttendanceSession.id)).join(
                    DisciplinePlan, AttendanceSession.discipline_plan_id == DisciplinePlan.id
                ).where(
                    and_(
                        DisciplinePlan.work_group_id.in_(group_ids),
                        AttendanceSession.date >= start_date,
                        AttendanceSession.date <= today
                    )
                )
                
                sessions_count_result = await db.execute(sessions_count_query)
                total_sessions = sessions_count_result.scalar() or 0
                
                if total_sessions == 0:
                    period_stats.append({
                        "direction": direction_name,
                        "attendance": 0.0
                    })
                    continue
                
                # Получаем количество посещений для данного направления в указанный период
                attendance_count_query = select(func.count(Attendance.id)).join(
                    Student, Attendance.student_id == Student.id
                ).join(
                    BaseGroup, Student.base_group_id == BaseGroup.id
                ).join(
                    AttendanceSession, Attendance.attendance_session_id == AttendanceSession.id
                ).join(
                    DisciplinePlan, AttendanceSession.discipline_plan_id == DisciplinePlan.id
                ).where(
                    and_(
                        BaseGroup.track_id == track_id,
                        AttendanceSession.date >= start_date,
                        AttendanceSession.date <= today
                    )
                )
                
                attendance_count_result = await db.execute(attendance_count_query)
                total_attendances = attendance_count_result.scalar()
                
                # Вычисляем процент посещаемости
                # Ожидаемое количество посещений = количество студентов * количество занятий
                expected_attendances = total_students * total_sessions
                
                if expected_attendances > 0:
                    attendance_percentage = min(100.0, (total_attendances / expected_attendances) * 100)
                else:
                    attendance_percentage = 0.0
                
                period_stats.append({
                    "direction": direction_name,
                    "attendance": round(attendance_percentage, 2)
                })
            
            result[period_name] = period_stats
        
        return result
        
    except Exception as e:
        raise Exception(f"Error calculating direction attendance stats: {str(e)}")

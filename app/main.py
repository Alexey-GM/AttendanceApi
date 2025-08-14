from fastapi import FastAPI
from app.api.auth.auth_routes import router as auth_router
from app.api.attendance import discipline_plan_router, attendance_session_router, course_stats_router, direction_stats_router, students_risk_router, group_attendance_router, four_weeks_router, student_attendance_router, general_attendance_router
from app.api.students import students_router

app = FastAPI()

app.include_router(auth_router, prefix="/api/auth")
app.include_router(discipline_plan_router, prefix="/api/attendance")
app.include_router(attendance_session_router, prefix="/api/attendance")
app.include_router(course_stats_router, prefix="/api/attendance")
app.include_router(direction_stats_router, prefix="/api/attendance")
app.include_router(students_risk_router, prefix="/api/attendance")
app.include_router(group_attendance_router, prefix="/api/attendance")
app.include_router(four_weeks_router, prefix="/api/attendance")
app.include_router(student_attendance_router, prefix="/api/attendance")
app.include_router(general_attendance_router, prefix="/api/attendance")
app.include_router(students_router, prefix="/api") 
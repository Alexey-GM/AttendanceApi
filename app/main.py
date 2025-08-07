from fastapi import FastAPI
from app.api.auth.auth_routes import router as auth_router
from app.api.attendance import discipline_plan_router, attendance_session_router
from app.api.students import students_router

app = FastAPI()

app.include_router(auth_router, prefix="/api/auth")
app.include_router(discipline_plan_router, prefix="/api/attendance")
app.include_router(attendance_session_router, prefix="/api/attendance")
app.include_router(students_router, prefix="/api") 
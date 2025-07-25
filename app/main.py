from fastapi import FastAPI
from app.api.auth.auth_routes import router as auth_router
from app.api.attendance import discipline_plan_router

app = FastAPI()

app.include_router(auth_router, prefix="/api/auth")
app.include_router(discipline_plan_router, prefix="/api/attendance") 
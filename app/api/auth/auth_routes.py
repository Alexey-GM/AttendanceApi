from fastapi import APIRouter, Depends, Request
from app.schemas.auth import UserCreate, UserLogin, TokenResponse
from app.services.auth_service import register_user, login_user
from app.utils.response import format_response
from fastapi.responses import JSONResponse
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.lecturer import Lecturer
from sqlalchemy import select
from datetime import timedelta
from app.utils.jwt import create_access_token
import bcrypt

router = APIRouter()

@router.post("/register")
async def register(user: UserCreate, request: Request, db: AsyncSession = Depends(get_db)):
    try:
        data = await register_user(user, db)
        return format_response(data=data, message="Registration successful", code=200)
    except Exception as e:
        return format_response(message=str(e), code=400)

@router.post("/login")
async def login(user: UserLogin, request: Request, db: AsyncSession = Depends(get_db)):
    try:
        response = await login_user(user, db)
        return format_response(data=response, message="Login successful", code=200)
    except Exception as e:
        return format_response(message=str(e), code=400) 
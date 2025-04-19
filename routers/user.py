from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestForm
from routers.jwt_handler import create_access_token
from typing import Optional
from  data.response import format_response
from data.db.db import get_db
from service.user_service import (
    login_user, register_user, change_password, edit_user_fio, fetch_teachers
)

router = APIRouter(prefix="/users", tags=["users"])

class UserLogin(BaseModel):
    login: str
    password: str

class UserRegister(BaseModel):
    first_name: str
    last_name: str
    patronymic: Optional[str]
    login: str
    password: str

class PasswordUpdate(BaseModel):
    old_password: str
    new_password: str

class UserFIOUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    patronymic: Optional[str]

@router.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)):
    try:
        new_user = register_user(db, user.dict())
        return format_response(
            data={"id": new_user.id, "login": new_user.login},
            message="User registered successfully",
            code=201
        )
    except Exception as e:
        print(f"Registration error: {e}")  # <-- временно для отладки
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = login_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid login or password")

    access_token = create_access_token(data={
        "sub": user.login,
        "user_id": user.id,
        "role": user.role
    })

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.put("/{user_id}/password")
def update_password(user_id: int, pwd: PasswordUpdate, db: Session = Depends(get_db)):
    updated = change_password(db, user_id, pwd.old_password, pwd.new_password)
    if not updated:
        raise HTTPException(status_code=403, detail="Old password is incorrect")
    return {"message": "Password updated successfully"}

@router.put("/{user_id}/edit-fio")
def update_fio(user_id: int, fio: UserFIOUpdate, db: Session = Depends(get_db)):
    user = edit_user_fio(db, user_id, fio.dict(exclude_unset=True))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "patronymic": user.patronymic
    }

@router.get("/teachers")
def get_teachers(db: Session = Depends(get_db)):
    teachers = fetch_teachers(db)
    return [
        {
            "id": t.id,
            "first_name": t.first_name,
            "last_name": t.last_name,
            "patronymic": t.patronymic,
            "login": t.login
        } for t in teachers
    ]

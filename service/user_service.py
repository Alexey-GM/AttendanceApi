from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from repository.user_repository import (
    get_user_by_login,
    create_user,
    update_password,
    update_user_fio,
    get_all_teachers,
)

def login_user(db: Session, login: str, password: str):
    try:
        user = get_user_by_login(db, login)
        if not user:
            raise ValueError("Invalid login or password")
            
        if not bcrypt.verify(password, user.password):
            raise ValueError("Invalid login or password")
            
        return user
    except Exception as e:
        raise ValueError(f"Service error during login: {str(e)}")

def register_user(db: Session, user_data: dict):
    try:
        required_fields = ["first_name", "last_name", "login", "password"]
        if not all(field in user_data for field in required_fields):
            raise ValueError("Missing required fields")
            
        existing_user = get_user_by_login(db, user_data["login"])
        if existing_user:
            raise ValueError("User already exists")
            
        return create_user(db, user_data)
    except Exception as e:
        raise ValueError(f"Service error during registration: {str(e)}")

def change_password(db: Session, user_id: int, old_password: str, new_password: str):
    try:
        if not old_password or not new_password:
            raise ValueError("Both old and new passwords are required")
            
        return update_password(db, user_id, old_password, new_password)
    except Exception as e:
        raise ValueError(f"Service error changing password: {str(e)}")

def edit_user_fio(db: Session, user_id: int, fio_data: dict):
    try:
        if not any(field in fio_data for field in ["first_name", "last_name", "patronymic"]):
            raise ValueError("At least one field must be provided")
            
        return update_user_fio(db, user_id, fio_data)
    except Exception as e:
        raise ValueError(f"Service error updating user info: {str(e)}")

def fetch_teachers(db: Session):
    try:
        teachers = get_all_teachers(db)
        return [
            {
                "id": t.id,
                "first_name": t.first_name,
                "last_name": t.last_name,
                "patronymic": t.patronymic,
                "login": t.login
            } for t in teachers
        ]
    except Exception as e:
        raise ValueError(f"Service error fetching teachers: {str(e)}")

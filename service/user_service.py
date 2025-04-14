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
    user = get_user_by_login(db, login)
    if user and user.password and user.password != "" and user.password != "null":
        if bcrypt.verify(password, user.password):
            return user
    return None

def register_user(db: Session, user_data: dict):
    return create_user(db, user_data)

def change_password(db: Session, user_id: int, old_password: str, new_password: str):
    return update_password(db, user_id, old_password, new_password)

def edit_user_fio(db: Session, user_id: int, fio_data: dict):
    return update_user_fio(db, user_id, fio_data)

def fetch_teachers(db: Session):
    return get_all_teachers(db)

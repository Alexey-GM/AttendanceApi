from pydantic import BaseModel

class UserCreate(BaseModel):
    login: str
    password: str
    first_name: str
    last_name: str
    middle_name: str | None = None
    department_id: int

class UserLogin(BaseModel):
    login: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer" 
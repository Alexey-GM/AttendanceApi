from pydantic import BaseModel
from datetime import date
from typing import Optional

class StudentResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    date_birth: Optional[str] = None  # Изменено на str для ISO формата
    base_group_id: int

    class Config:
        from_attributes = True 
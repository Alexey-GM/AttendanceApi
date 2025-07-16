from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from service.risk_students_service import fetch_risk_students
from data.response import format_response
from data.db.db import get_db
from typing import List
from pydantic import BaseModel

router = APIRouter(prefix="/risk_students", tags=["risk_students"])

class RiskStudent(BaseModel):
    full_name: str
    group: str
    missed: int

class RiskStudentsResponse(BaseModel):
    timestamp: str
    message: str
    code: int
    data: List[RiskStudent]

@router.get("/", response_model=RiskStudentsResponse)
def get_risk_students(db: Session = Depends(get_db)):
    risk_data = fetch_risk_students(db)
    return format_response(data=risk_data, message="OK", code=200)

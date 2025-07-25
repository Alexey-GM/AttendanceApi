from sqlalchemy import Column, Integer, String
from app.models.lecturer import Base

class AttendanceStatus(Base):
    __tablename__ = "attendance_status"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    comment = Column(String) 
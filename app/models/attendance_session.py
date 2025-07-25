from sqlalchemy import Column, Integer, Date, ForeignKey
from app.models.lecturer import Base

class AttendanceSession(Base):
    __tablename__ = "attendance_session"
    id = Column(Integer, primary_key=True)
    discipline_plan_id = Column(Integer, ForeignKey("discipline_plan.id"), nullable=False)
    date = Column(Date, nullable=False)
    classroom_id = Column(Integer, ForeignKey("classroom.id"), nullable=False) 
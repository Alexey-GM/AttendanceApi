from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from app.models.lecturer import Base

class Attendance(Base):
    __tablename__ = "attendance"
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("student.id"), nullable=False)
    attendance_session_id = Column(Integer, ForeignKey("attendance_session.id"), nullable=False)
    attendance_status_id = Column(Integer, ForeignKey("attendance_status.id"), nullable=False)
    attendance_timestamp = Column(DateTime, nullable=False)
    comment = Column(String) 
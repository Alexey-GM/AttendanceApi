from sqlalchemy import Column, Integer, Date, Boolean, ForeignKey
from app.models.lecturer import Base

class GroupEnrollment(Base):
    __tablename__ = "group_enrollment"
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("student.id"), nullable=False)
    work_group_id = Column(Integer, ForeignKey("work_group.id"), nullable=False)
    academic_year_id = Column(Integer, ForeignKey("academic_year.id"), nullable=False)
    enrollment_date = Column(Date, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True) 
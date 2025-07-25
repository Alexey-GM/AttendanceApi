from sqlalchemy import Column, Integer, String, Date, Boolean
from app.models.lecturer import Base

class AcademicYear(Base):
    __tablename__ = "academic_year"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    date_start = Column(Date, nullable=False)
    date_end = Column(Date, nullable=False)
    is_current = Column(Boolean, nullable=False, default=False) 
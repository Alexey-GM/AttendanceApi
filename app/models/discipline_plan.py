from sqlalchemy import Column, Integer, ForeignKey
from app.models.lecturer import Base

class DisciplinePlan(Base):
    __tablename__ = "discipline_plan"
    id = Column(Integer, primary_key=True)
    lecturer_id = Column(Integer, ForeignKey("lecturer.id"), nullable=False)
    work_group_id = Column(Integer, ForeignKey("work_group.id"), nullable=False)
    discipline_id = Column(Integer, ForeignKey("discipline.id"), nullable=False)
    activity_type_id = Column(Integer, ForeignKey("activity_type.id"), nullable=False)
    academic_hours = Column(Integer, nullable=False) 
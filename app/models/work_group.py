from sqlalchemy import Column, Integer, String, ForeignKey
from app.models.lecturer import Base

class WorkGroup(Base):
    __tablename__ = "work_group"
    id = Column(Integer, primary_key=True)
    base_group_id = Column(Integer, ForeignKey("base_group.id"), nullable=False)
    name = Column(String, nullable=False)
    comment = Column(String) 
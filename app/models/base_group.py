from sqlalchemy import Column, Integer, String, ForeignKey
from app.models.lecturer import Base

class BaseGroup(Base):
    __tablename__ = "base_group"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    intake_year = Column(Integer, nullable=False)
    course_number = Column(Integer, nullable=False)
    track_id = Column(Integer, ForeignKey("track.id"), nullable=False) 
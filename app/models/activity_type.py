from sqlalchemy import Column, Integer, String
from app.models.lecturer import Base

class ActivityType(Base):
    __tablename__ = "activity_type"
    id = Column(Integer, primary_key=True)
    short_name = Column(String, nullable=False)
    full_name = Column(String, nullable=False) 
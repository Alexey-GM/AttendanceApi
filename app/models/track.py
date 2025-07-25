from sqlalchemy import Column, Integer, String, ForeignKey
from app.models.lecturer import Base

class Track(Base):
    __tablename__ = "track"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    specialty_id = Column(Integer, ForeignKey("specialty.id"), nullable=False) 
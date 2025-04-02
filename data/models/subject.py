from sqlalchemy import Column, Integer, String
from data.db.db import Base

class Subject(Base):
    __tablename__ = "subject"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    lecturer = Column(String(100))
    hours = Column(Integer)
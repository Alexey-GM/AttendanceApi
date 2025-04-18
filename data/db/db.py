from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from pydantic_settings import BaseSettings
from sqlalchemy.exc import SQLAlchemyError

# создаем базу данных
class Settings(BaseSettings):
    DATABASE_URL: str

    class Config:
        env_file = ".env" 

        extra = "allow"  

settings = Settings()

# создаем движок базы данных
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        db.rollback()
        raise ValueError(f"Database error: {str(e)}")
    finally:
        db.close()

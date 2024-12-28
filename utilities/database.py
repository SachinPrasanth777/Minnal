from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from schemas.models import database

class Database():
    def __init__(self):
        settings = database()
        self.DB_URL = f"postgresql://{settings.DB_USERNAME}:{settings.DB_PASSWORD}@postgres:5432/{settings.DB_NAME}"
        self.engine = create_engine(self.DB_URL)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.base = declarative_base()
    
    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()
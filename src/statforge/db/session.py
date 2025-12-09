from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from statforge.config.settings import get_settings

settings = get_settings()

engine = create_engine(settings.sqlalchemy_database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

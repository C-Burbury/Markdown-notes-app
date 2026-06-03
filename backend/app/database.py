from sqlalchemy import create_engine
from app.config import settings
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import sessionmaker



url_string = str(settings.DATABASE_URL)

engine = create_engine(url_string)

class Base(DeclarativeBase):
    pass

SessionLocal = sessionmaker(bind=engine)
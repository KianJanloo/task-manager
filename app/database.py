from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


DATABASE_URL = "sqlite:///./task_manager.db"


class Base(DeclarativeBase):
    pass


engine = create_engine(DATABASE_URL)


SessionLocal = sessionmaker(
    bind=engine,
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

from app.models.task import Task
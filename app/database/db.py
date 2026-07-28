import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependency generator that yields a database session and ensures proper closure.

    Yields:
        Session: SQLAlchemy database session instance.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

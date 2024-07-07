from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

Base = declarative_base()


def db_name():
    return f"sqlite:///{os.getenv('DB_NAME')}.db"


def get_engine():
    return create_engine(db_name(), echo=True)


def get_session():
    engine = create_engine(db_name(), echo=True)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()


def migration():
    engine = create_engine(db_name(), echo=True)
    Base.metadata.create_all(bind=engine)

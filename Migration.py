from model import Model
from sqlalchemy import create_engine
from model.engine.Engine import migration
from sqlalchemy.orm import sessionmaker, declarative_base

migration()

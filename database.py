from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from config import Config
from typing import Annotated
from fastapi import Depends

# DB_URL = 'sqlite:///./blog.db'

engine = create_engine(Config.SQLALCHEMY_URL, connect_args={"check_same_thread": False})

SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON;")
    cursor.close()

def get_db_session():
    db_session = SessionFactory()
    try:
        yield db_session
    finally:
        db_session.close()

db_dependency = Annotated[Session, Depends(get_db_session)]
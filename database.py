from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

DB_URL = 'sqlite:///./blog.db'

engine = create_engine(DB_URL, connect_args={"check_same_thread": False})

SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db_session():
    db_session = SessionFactory()
    try:
        yield db_session
    finally:
        db_session.close()



import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv


load_dotenv()


SQLALCHEMY_DATABASE_URL =os.environ.get('SQLALCHEMY_DATABASE_URL')

#for docker
# username=os.environ.get('DATABASE_NAME')
# pwd = os.environ.get('DATABASE_PASSWORD')
# host=os.environ.get('DATABASE_HOSTNAME')
# port = os.environ.get('DATABASE_POST')
# db_name=os.environ.get('DATABASE_NAME')
# SQLALCHEMY_DATABASE_URL = f"postgresql://{username}:{pwd}@{host}:{port}/{db_name}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
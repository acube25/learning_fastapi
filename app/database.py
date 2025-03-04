from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

# SQLALCHEMY_DATABASE_URL = f"postgresql://acube:absudur@localhost:5432/fast_api_with_Sanjeev"
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"


engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit = False, autoflush= False, bind= engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()


# while True:
#     try:
#         conn = psycopg2.connect(host = "localhost", database = "fast_api_with_Sanjeev", user = "postgres", 
#                                 password = "absudur1fs", cursor_factory = RealDictCursor)
#         cursor = conn.cursor()
#         print("Database Connection was succesfull")
#         break
#     except Exception as error: 
#         print("Database connection was failed")
#         print("Error: ", error)
#         time.sleep(2)
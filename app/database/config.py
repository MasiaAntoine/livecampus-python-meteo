import os
import time

import pymysql
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_CONFIG = {
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'host': os.getenv('MYSQL_HOST'),
    'database': os.getenv('MYSQL_DATABASE'),
    'port': "3306",
}

def wait_for_db(max_retries=30, delay_seconds=2):
    retries = 0
    while retries < max_retries:
        try:
            conn = pymysql.connect(
                host=DATABASE_CONFIG['host'],
                user=DATABASE_CONFIG['user'],
                password=DATABASE_CONFIG['password'],
                port=int(DATABASE_CONFIG['port'])
            )
            conn.close()
            print("Database is ready!")
            return True
        except pymysql.Error as e:
            retries += 1
            print(f"Database not ready yet (attempt {retries}/{max_retries}). Waiting {delay_seconds} seconds...")
            time.sleep(delay_seconds)

    raise RuntimeError("Could not connect to the database after maximum retries")

for key, value in DATABASE_CONFIG.items():
    if value is None:
        raise ValueError(f"Missing required environment variable for database configuration: {key}")

DATABASE_URL = f"mysql+pymysql://{DATABASE_CONFIG['user']}:{DATABASE_CONFIG['password']}@{DATABASE_CONFIG['host']}:{DATABASE_CONFIG['port']}/{DATABASE_CONFIG['database']}"

wait_for_db()

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
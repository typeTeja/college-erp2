from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

load_dotenv("apps/api/.env")
db_url = os.getenv("DATABASE_URL")

engine = create_engine(db_url)

def check_enum():
    with engine.connect() as conn:
        print("Checking enum 'applicationstatus'...")
        result = conn.execute(text("SELECT enumlabel FROM pg_enum JOIN pg_type ON pg_enum.enumtypid = pg_type.oid WHERE pg_type.typname = 'applicationstatus';"))
        labels = [row[0] for row in result]
        print(f"Values in 'applicationstatus': {labels}")

if __name__ == "__main__":
    check_enum()

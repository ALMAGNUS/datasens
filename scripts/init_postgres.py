import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv


def get_engine():
    load_dotenv()
    url = os.getenv("DATASENS_DB_URL", "postgresql+psycopg2://postgres:postgres@localhost:5432/datasens")
    return create_engine(url, future=True)


def ensure_database():
    engine = get_engine()
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))


if __name__ == "__main__":
    ensure_database()
    print("PostgreSQL connection ok.")



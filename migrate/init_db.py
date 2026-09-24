import os, time, psycopg2
from pathlib import Path
from dotenv import load_dotenv


load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PWD = os.getenv("DB_PWD")

SCHEMA_FILE = Path(__file__).parent / "big_fat_schema.sql" #TODO: clean it up

def connect_with_retry(max_retries=3, delay= 2):
    for attempt in range (0, max_retries):
        try:
            conn = psycopg2.connect(
                host = DB_HOST,
                port = DB_PORT,
                dbname = DB_NAME,
                user = DB_USER,
                password = DB_PWD
            )
            print(f"connected at {DB_HOST}:{DB_PORT}")
            return conn
        except psycopg2.OperationalError as e:
            print(({e}))
            print(f"Attempt: {attempt}/{max_retries} retrying in {delay}")
        time.sleep(delay)
    raise TimeoutError("did not connect, check error")

def init_db():
    if not SCHEMA_FILE.exists():
        raise FileNotFoundError(f'no schema file found matching filename: {SCHEMA_FILE}')

    with open(SCHEMA_FILE, 'r', encoding="utf-8") as f:
        sql_script = f.read()

    conn = connect_with_retry()
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql_script)
        conn.commit()
        print("schema init with no issues")
    except Exception as e:
        conn.rollback()
        print(f"init failed, rolling back, failed due to {e}")
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    init_db()

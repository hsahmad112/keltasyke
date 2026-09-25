from s02_init_db import connect_with_retry
from pathlib import Path

UT = Path(__file__).parent / "user_tables.sql"

conn = connect_with_retry()


if not UT.exists():
    raise FileNotFoundError(f'no file found matching {UT}')
with open(UT, 'r', encoding="utf-8") as f:
    sql_script = f.read()

with conn.cursor() as cursor:
    cursor.execute(sql_script)
conn.commit()

print('done. shame on your for not implementing try/excepts here >:I')
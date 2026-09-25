import os, time, psycopg2
from pathlib import Path
from dotenv import load_dotenv
from init_db import connect_with_retry



def clean_db():
    conn = connect_with_retry()

    try:
        with conn.cursor() as cursor:
            cursor.execute("""TRUNCATE TABLE agency, calendar, calendar_dates, routes, stop_times, stops, stops_translations, trips_headsign_translations, trip_notes, trips""")
    except Exception as e:
        conn.rollback()
        print(f"cleaning failed, rolling back, failed due to {e}")
        raise
    finally:
        print("cleaned successfully: agency, calendar, calendar_dates, routes, stop_times, stops, stops_translations, trips_headsign_translations, trip_notes and trips" )
        conn.close()

if __name__ == "__main__":
    clean_db()

import os, time, psycopg2, sys
from pathlib import Path
from dotenv import load_dotenv
from s02_init_db import connect_with_retry



def clean_static_tables():
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


def clean_user_tables():
    conn = connect_with_retry()
    
    try:
        with conn.cursor() as cursor:
            cursor.execute("""TRUNCATE TABLE preferences, service_alerts""")
    except Exception as e:
        conn.rollback()
        print(f"cleaning failed, rolling back, failed due to {e}")
        raise
    finally:
        print("cleaned successfully: preferences and service_alerts" )
        conn.close() 

if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()

        if command == "user":
            clean_user_tables()
        elif command == "static":
            clean_static_tables()
        else:
            print(f"unk command, either add \"user\" or \"static\" or implement \"both\" if that is what you want")

    else:
        print("no command provided, dummy")
import os
import psycopg2
from transform_weather import load_raw_files, transform_file

def get_connection():
    return psycopg2.connect(
        host=os.environ.get("POSTGRES_HOST", "127.0.0.1"),
        port=os.environ.get("POSTGRES_PORT", "5433"),
        user="airflow",
        password="airflow",
        dbname="weather_db"
    )
def load_rows(rows):
    conn = get_connection()
    cur = conn.cursor()

    for row in rows:
        cur.execute("""
    INSERT INTO weather_daily (city, date, temp_max, temp_min, precipitation)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (city, date) DO UPDATE SET
        temp_max = EXCLUDED.temp_max,
        temp_min = EXCLUDED.temp_min,
        precipitation = EXCLUDED.precipitation
""", (row["city"], row["date"], row["temp_max"], row["temp_min"], row["precipitation"]))

    conn.commit()
    cur.close()
    conn.close()
    print(f"Loaded {len(rows)} rows into weather_daily")

if __name__ == "__main__":
    files = load_raw_files()
    all_rows = []
    for filepath in files:
        all_rows.extend(transform_file(filepath))

    load_rows(all_rows)
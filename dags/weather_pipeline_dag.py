from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

sys.path.append('/opt/airflow/scripts')

from extract_weather import fetch_weather, save_raw_data
from transform_weather import load_raw_files, transform_file
from load_to_postgres import load_rows

def run_extract():
    cities = {
        "Hargeisa": (9.5600, 44.0650),
        "Nairobi": (-1.2864, 36.8172),
        "Addis_Ababa": (9.0250, 38.7469),
        "Mogadishu": (2.0469, 45.3182),
    }
    for city, (lat, lon) in cities.items():
        data = fetch_weather(city, lat, lon)
        save_raw_data(city, data)

def run_transform_and_load():
    files = load_raw_files()
    all_rows = []
    for filepath in files:
        all_rows.extend(transform_file(filepath))
    load_rows(all_rows)

default_args = {
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'weather_pipeline',
    schedule='@daily',
    start_date=datetime(2026, 9, 1),
    catchup=False,
    default_args=default_args,
) as dag:

    extract_task = PythonOperator(
        task_id='extract',
        python_callable=run_extract,
    )

    load_task = PythonOperator(
        task_id='transform_and_load',
        python_callable=run_transform_and_load,
    )

    extract_task >> load_task
    
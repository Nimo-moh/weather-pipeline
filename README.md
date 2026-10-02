# East Africa Weather Pipeline

An end-to-end data engineering pipeline that extracts daily weather data for East African cities, transforms and validates it, and loads it into PostgreSQL fully orchestrated with Apache Airflow.

## Problem

Raw data from external APIs is rarely analysis-ready. This project builds a reliable, automated pipeline that handles the full lifecycle of that data: fetching it on a schedule, cleaning and validating it, and storing it safely — including handling failures and repeated runs without corrupting data.

## Architecture

Open-Meteo API
|
v
[extract] --> raw JSON saved to data/raw/
|
v
[transform] --> clean, validate, reshape into rows
|
v
[load] --> upsert into PostgreSQL (idempotent)
|
v
Orchestrated daily by Airflow, with retries on failure

## Technologies

- **Python** — extraction, transformation, and loading logic
- **PostgreSQL** — structured storage
- **Apache Airflow** — orchestration and scheduling
- **Docker / Docker Compose** — containerized, reproducible environment
- **Open-Meteo API** — free, no-auth weather data source

## Data

Daily weather data (max/min temperature, precipitation) for four East African cities: Hargeisa, Nairobi, Addis Ababa, and Mogadishu.

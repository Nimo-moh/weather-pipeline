import json
import os
import glob

def load_raw_files(city=None):
    """Load all raw JSON files, optionally filtered by city."""
    pattern = f"data/raw/{city}_*.json" if city else "data/raw/*.json"
    files = glob.glob(pattern)
    return files

def transform_file(filepath):
    """Read one raw JSON file and reshape it into clean rows."""
    with open(filepath, "r") as f:
        raw = json.load(f)

    city = os.path.basename(filepath).split("_")[0]
    daily = raw["daily"]

    rows = []
    for i in range(len(daily["time"])):
        row = {
            "city": city,
            "date": daily["time"][i],
            "temp_max": daily["temperature_2m_max"][i],
            "temp_min": daily["temperature_2m_min"][i],
            "precipitation": daily["precipitation_sum"][i],
        }
        # Validation: skip rows with missing critical data
        if row["temp_max"] is None or row["temp_min"] is None:
            print(f"Skipping invalid row: {row}")
            continue
        rows.append(row)

    return rows

if __name__ == "__main__":
    files = load_raw_files()
    print(f"Found {len(files)} raw files")

    all_rows = []
    for filepath in files:
        rows = transform_file(filepath)
        all_rows.extend(rows)

    print(f"Transformed {len(all_rows)} total rows")
    print(all_rows[:3])  # preview first 3 rows
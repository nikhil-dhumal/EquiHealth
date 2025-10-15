import csv
import os
import sys

# Ensure we can import app + models
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app, db
from models import District

# Path to your CSV file
CSV_FILE = "../../data/maharashtra/district.csv"


def clean_str(value):
    """Return clean string or None."""
    if not value or str(value).strip() in ("", "nan", "NaN", "None"):
        return None
    return str(value).strip()


def clean_int(value):
    """Safely convert numeric-looking strings to int."""
    try:
        if value is None or str(value).strip() == "":
            return None
        return int(float(value))
    except Exception:
        return None


def clean_float(value):
    """Safely convert to float or return None."""
    try:
        if value is None or str(value).strip() == "":
            return None
        return float(value)
    except Exception:
        return None


def populate_districts():
    with app.app_context():
        with open(CSV_FILE, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            count_inserted, count_skipped = 0, 0

            for row in reader:
                district_id = clean_int(row.get("district_id"))
                district_name = clean_str(row.get("district_name"))
                state_name = clean_str(row.get("state_name"))

                # Check for existing district by (district_id)
                existing = District.query.filter_by(district_id=district_id).first()
                if existing:
                    print(f"Skipping existing district ID {district_id} ({existing.district_name})")
                    count_skipped += 1
                    continue

                district = District(
                    district_id=district_id,
                    district_name=district_name,
                    state_name=state_name,
                    latitude=clean_float(row.get("latitude")),
                    longitude=clean_float(row.get("longitude")),
                    total_persons=clean_int(row.get("total_persons")),
                    total_males=clean_int(row.get("total_males")),
                    total_females=clean_int(row.get("total_females")),
                    children_persons=clean_int(row.get("children_persons")),
                    children_males=clean_int(row.get("children_males")),
                    children_females=clean_int(row.get("children_females")),
                )

                db.session.add(district)
                count_inserted += 1

            db.session.commit()

            print("Districts table populated successfully!")
            print(f"Inserted: {count_inserted}")
            print(f"Skipped (duplicates): {count_skipped}")


if __name__ == "__main__":
    populate_districts()

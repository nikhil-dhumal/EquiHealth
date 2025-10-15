import csv
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app, db
from models import Hospital

# Configuration
CSV_FILE = "../../data/maharashtra/hospital.csv"
STATE_NAME = "Maharashtra"   # Change this if importing for another state


def clean_str(value):
    """Convert floats like 400701.0 or NaN to clean strings or None."""
    if not value or str(value).strip() in ("", "nan", "NaN", "None"):
        return None
    s = str(value).strip()
    if s.endswith(".0"):
        s = s[:-2]
    return s


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


def populate_hospitals():
    with app.app_context():
        with open(CSV_FILE, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            count_inserted, count_skipped = 0, 0

            for row in reader:
                hospital_id = clean_int(row.get("hospital_id"))
                district_id = clean_int(row.get("district_id"))

                # Composite PK check (hospital_id + state_name)
                existing = Hospital.query.filter_by(
                    hospital_id=hospital_id,
                    state_name=STATE_NAME
                ).first()

                if existing:
                    print(f"Skipping existing hospital ID {hospital_id} ({existing.hospital_name})")
                    count_skipped += 1
                    continue

                hospital = Hospital(
                    hospital_id=hospital_id,
                    state_name=STATE_NAME,
                    district_id=district_id,
                    hospital_name=row.get("hospital_name", "").strip(),
                    address=row.get("address", "").strip() or None,
                    pincode=clean_str(row.get("pincode")),
                    latitude=clean_float(row.get("latitude")),
                    longitude=clean_float(row.get("longitude")),
                    mco_contact_number=clean_str(row.get("mco_contact_number")),
                    total_beds=clean_int(row.get("total_beds")),
                    hospital_type=row.get("hospital_type", "").strip() or None,
                    government_subtype=row.get("government_subtype", "").strip() or None,
                )

                db.session.add(hospital)
                count_inserted += 1

            db.session.commit()

            print(f"Hospitals table populated successfully!")
            print(f"Inserted: {count_inserted}")
            print(f"Skipped (duplicates): {count_skipped}")


if __name__ == "__main__":
    populate_hospitals()
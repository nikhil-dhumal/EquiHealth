import os
import sys
import csv

# --- Ensure the parent directory is in the Python path ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app, db
from models import Hospital

# Path to the CSV file (in the same folder)
CSV_FILE = "../../data/maharashtra/hospital.csv"

def populate_hospitals():
    with app.app_context():
        with open(CSV_FILE, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                # Convert fields to Python types and clean data
                hospital_id = int(row["hospital_id"])
                pincode = str(row["pincode"]).split(".")[0] if row["pincode"] else None
                total_beds = int(float(row["total_beds"])) if row["total_beds"] else None

                # Check if already exists (composite key: hospital_id + state)
                existing = Hospital.query.get((hospital_id, "Maharashtra"))
                if existing:
                    print(f"Skipping existing hospital ID {hospital_id}: {row['hospital_name']}")
                    continue

                hospital = Hospital(
                    hospital_id=hospital_id,
                    state="Maharashtra",  # Default for all rows
                    hosp_disp_code=row["hosp_disp_code"].strip() if row["hosp_disp_code"] else None,
                    hospital_name=row["hospital_name"].strip(),
                    address=row["address"].strip() if row["address"] else None,
                    taluka=row["taluka"].strip() if row["taluka"] else None,
                    district=row["district"].strip() if row["district"] else None,
                    pincode=pincode,
                    mco_contact_number=str(row["mco_contact_number"]).split(".")[0] if row["mco_contact_number"] else None,
                    total_beds=total_beds,
                    hospital_type=row["hospital_type"].strip() if row["hospital_type"] else None,
                    government_sub_type=row["government_sub_type"].strip() if row["government_sub_type"] else None
                )

                db.session.add(hospital)

            db.session.commit()
            print("✅ Hospitals table populated successfully!")

if __name__ == "__main__":
    populate_hospitals()
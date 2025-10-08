import os
import sys
import csv

# --- Ensure parent directory (project root) is importable ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app, db
from models import Hospital, Category, hospital_category

CSV_FILE = "../../data/maharashtra/hospital_category.csv"

def populate_hospital_categories():
    with app.app_context():
        with open(CSV_FILE, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                hospital_id = int(row["hospital_id"])
                category_id = int(row["category_id"])
                state = "Maharashtra"  # default for all hospitals

                # Check if hospital and category exist
                hospital = Hospital.query.get((hospital_id, state))
                category = Category.query.get(category_id)

                if not hospital:
                    print(f"⚠️ Skipping: Hospital ID {hospital_id} not found in DB.")
                    continue
                if not category:
                    print(f"⚠️ Skipping: Category ID {category_id} not found in DB.")
                    continue

                # Check if relationship already exists
                existing = db.session.execute(
                    db.select(hospital_category).filter_by(
                        hospital_id=hospital_id, state=state, category_id=category_id
                    )
                ).first()

                if existing:
                    print(f"Skipping existing link: Hospital {hospital_id} ↔ Category {category_id}")
                    continue

                # Insert relationship manually into association table
                insert_stmt = hospital_category.insert().values(
                    hospital_id=hospital_id,
                    state=state,
                    category_id=category_id
                )
                db.session.execute(insert_stmt)

            db.session.commit()
            print("✅ Hospital–Category associations populated successfully!")

if __name__ == "__main__":
    populate_hospital_categories()

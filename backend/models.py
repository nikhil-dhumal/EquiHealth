# models.py
from app import db

# Association table for many-to-many relationship
hospital_category = db.Table(
    "hospital_category",
    db.Column("hospital_id", db.Integer, nullable=False),
    db.Column("state", db.String(100), nullable=False),
    db.Column("category_id", db.Integer, db.ForeignKey("category.category_id", ondelete="CASCADE"), nullable=False),
    db.ForeignKeyConstraint(
        ["hospital_id", "state"], ["hospital.hospital_id", "hospital.state"], ondelete="CASCADE"
    ),
    db.PrimaryKeyConstraint("hospital_id", "state", "category_id")
)

class Hospital(db.Model):
    __tablename__ = "hospital"

    hospital_id = db.Column(db.Integer, nullable=False)
    state = db.Column(db.String(100), nullable=False)

    hosp_disp_code = db.Column(db.String(100), nullable=True)
    hospital_name = db.Column(db.String(1024), nullable=False)
    address = db.Column(db.Text, nullable=True)
    taluka = db.Column(db.String(256), nullable=True)
    district = db.Column(db.String(256), nullable=True)
    pincode = db.Column(db.String(20), nullable=True)
    mco_contact_number = db.Column(db.String(50), nullable=True)
    total_beds = db.Column(db.Integer, nullable=True)
    hospital_type = db.Column(db.String(100), nullable=True)
    government_sub_type = db.Column(db.String(100), nullable=True)

    __table_args__ = (
        db.PrimaryKeyConstraint("hospital_id", "state"),
    )

    categories = db.relationship(
        "Category",
        secondary=hospital_category,
        back_populates="hospitals"
    )

    def to_dict(self):
        return {
            "hospital_id": self.hospital_id,
            "state": self.state,
            "hospital_name": self.hospital_name,
            "district": self.district,
        }

class Category(db.Model):
    __tablename__ = "category"

    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(255), nullable=False, unique=True)

    hospitals = db.relationship(
        "Hospital",
        secondary=hospital_category,
        back_populates="categories"
    )

    def to_dict(self):
        return {"category_id": self.category_id, "category_name": self.category_name}

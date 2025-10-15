# models.py
from app import db

# --- Association Table ---
hospital_category = db.Table(
    "hospital_category",
    db.Column("hospital_id", db.Integer, nullable=False),
    db.Column("state_name", db.String(128), nullable=False),
    db.Column("category_id", db.Integer, db.ForeignKey("category.category_id", ondelete="CASCADE"), nullable=False),
    db.ForeignKeyConstraint(
        ["hospital_id", "state_name"],
        ["hospital.hospital_id", "hospital.state_name"],
        ondelete="CASCADE"
    ),
    db.PrimaryKeyConstraint("hospital_id", "state_name", "category_id")
)

# --- District ---
class District(db.Model):
    __tablename__ = "district"

    district_id = db.Column(db.Integer, primary_key=True)
    district_name = db.Column(db.String(256), nullable=False, index=True)
    state_name = db.Column(db.String(128), nullable=False, index=True)

    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    total_persons = db.Column(db.Integer, nullable=True)
    total_males = db.Column(db.Integer, nullable=True)
    total_females = db.Column(db.Integer, nullable=True)
    children_persons = db.Column(db.Integer, nullable=True)
    children_males = db.Column(db.Integer, nullable=True)
    children_females = db.Column(db.Integer, nullable=True)

    hospitals = db.relationship(
        "Hospital",
        back_populates="district",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    def to_dict(self):
        return {
            "district_id": self.district_id,
            "district_name": self.district_name,
            "state_name": self.state_name,
        }

# --- Hospital ---
class Hospital(db.Model):
    __tablename__ = "hospital"

    hospital_id = db.Column(db.Integer, nullable=False)
    state_name = db.Column(db.String(128), nullable=False)

    district_id = db.Column(
        db.Integer,
        db.ForeignKey("district.district_id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )

    hospital_name = db.Column(db.String(1024), nullable=False)
    address = db.Column(db.Text, nullable=True)
    pincode = db.Column(db.String(20), nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    mco_contact_number = db.Column(db.String(50), nullable=True)
    total_beds = db.Column(db.Integer, nullable=True)
    hospital_type = db.Column(db.String(100), nullable=True)
    government_subtype = db.Column(db.String(100), nullable=True)

    __table_args__ = (
        db.PrimaryKeyConstraint("hospital_id", "state_name"),
    )

    district = db.relationship("District", back_populates="hospitals")

    categories = db.relationship(
        "Category",
        secondary=hospital_category,
        back_populates="hospitals"
    )

    def to_dict(self):
        return {
            "hospital_id": self.hospital_id,
            "state_name": self.state_name,
            "district_id": self.district_id,
            "hospital_name": self.hospital_name,
            "address": self.address,
            "pincode": self.pincode,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "mco_contact_number": self.mco_contact_number,
            "total_beds": self.total_beds,
            "hospital_type": self.hospital_type,
            "government_subtype": self.government_subtype,
        }

# --- Category ---
class Category(db.Model):
    __tablename__ = "category"

    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100), nullable=False, unique=True)

    hospitals = db.relationship(
        "Hospital",
        secondary=hospital_category,
        back_populates="categories"
    )

    def to_dict(self):
        return {
            "category_id": self.category_id,
            "category_name": self.category_name
        }

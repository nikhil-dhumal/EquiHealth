from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime

from extensions import db

# Association Table (composite FK -> hospital)
hospital_category = db.Table(
    "hospital_category",
    db.Column("hospital_id", db.Integer, nullable=False),
    db.Column("state_id", db.Integer, nullable=False),
    db.Column("category_id", db.Integer, db.ForeignKey("category.category_id", ondelete="CASCADE"), nullable=False),
    db.ForeignKeyConstraint(
        ["hospital_id", "state_id"],
        ["hospital.hospital_id", "hospital.state_id"],
        ondelete="CASCADE",
    ),
    db.PrimaryKeyConstraint("hospital_id", "state_id", "category_id"),
)

# State
class State(db.Model):
    __tablename__ = "state"

    state_id = db.Column(db.Integer, primary_key=True)
    state_name = db.Column(db.String(128), nullable=False, unique=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)

    districts = db.relationship(
        "District",
        back_populates="state",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    hospitals = db.relationship(
        "Hospital",
        back_populates="state",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def to_dict(self):
        return {
            "state_id": self.state_id,
            "state_name": self.state_name,
            "latitude": self.latitude,
            "longitude": self.longitude,
        }

# District
class District(db.Model):
    __tablename__ = "district"

    district_id = db.Column(db.Integer, primary_key=True)
    state_id = db.Column(
        db.Integer,
        db.ForeignKey("state.state_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    district_name = db.Column(db.String(256), nullable=False, index=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    total_persons = db.Column(db.Integer, nullable=True)
    total_males = db.Column(db.Integer, nullable=True)
    total_females = db.Column(db.Integer, nullable=True)
    children_persons = db.Column(db.Integer, nullable=True)
    children_males = db.Column(db.Integer, nullable=True)
    children_females = db.Column(db.Integer, nullable=True)

    state = db.relationship("State", back_populates="districts")

    hospitals = db.relationship(
        "Hospital",
        back_populates="district",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def to_dict(self):
        return {
            "district_id": self.district_id,
            "district_name": self.district_name,
            "state_id": self.state_id,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "total_persons": self.total_persons,
            "total_males": self.total_males,
            "total_females": self.total_females,
            "children_persons": self.children_persons,
            "children_males": self.children_males,
            "children_females": self.children_females
        }

# Hospital (composite PK: hospital_id + state_id)
class Hospital(db.Model):
    __tablename__ = "hospital"

    hospital_id = db.Column(db.Integer, nullable=False)
    state_id = db.Column(
        db.Integer,
        db.ForeignKey("state.state_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    district_id = db.Column(
        db.Integer,
        db.ForeignKey("district.district_id", ondelete="SET NULL"),
        nullable=True,
        index=True,
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
        db.PrimaryKeyConstraint("hospital_id", "state_id"),
    )

    district = db.relationship("District", back_populates="hospitals")
    state = db.relationship("State", back_populates="hospitals")

    categories = db.relationship(
        "Category",
        secondary=hospital_category,
        back_populates="hospitals",
    )

    def to_dict(self):
        return {
            "hospital_id": self.hospital_id,
            "state_id": self.state_id,
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

# Category
class Category(db.Model):
    __tablename__ = "category"

    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100), nullable=False, unique=True)

    hospitals = db.relationship(
        "Hospital",
        secondary=hospital_category,
        back_populates="categories",
    )

    def to_dict(self):
        return {
            "category_id": self.category_id,
            "category_name": self.category_name,
        }

################### Complaints Model

class User(db.Model):
    __tablename__ = "user"

    # Columns
    phone_number = db.Column(db.String(20), primary_key=True, nullable=False, index=True)
    name = db.Column(db.String(128), nullable=False)
    details = db.Column(JSONB, nullable=True)

    def to_dict(self):
        return {
            "phone_number": self.phone_number,
            "name": self.name,
            "details": self.details or {}
        }



class Complaint(db.Model):
    __tablename__ = "complaint"

    complaint_id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    # User details
    mobile = db.Column(db.String(20), nullable=False, index=True)
    name = db.Column(db.String(128), nullable=False)

    # Foreign keys
    state_id = db.Column(db.Integer, db.ForeignKey("state.state_id", ondelete="SET NULL"), nullable=True)
    district_id = db.Column(db.Integer, db.ForeignKey("district.district_id", ondelete="SET NULL"), nullable=True)
    hospital_id = db.Column(db.Integer, nullable=True)

    # Complaint details
    title = db.Column(db.String(256), nullable=False)
    details = db.Column(db.Text, nullable=True)

    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    state = db.relationship("State", backref="complaints", lazy=True)
    district = db.relationship("District", backref="complaints", lazy=True)

    __table_args__ = (
        db.Index("idx_complaints_state", "state_id"),
        db.Index("idx_complaints_district", "district_id"),
        db.Index("idx_complaints_hospital", "hospital_id"),
    )

    def to_dict(self):
        return {
            "complaint_id": self.complaint_id,
            "mobile": self.mobile,
            "name": self.name,
            "state_id": self.state_id,
            "district_id": self.district_id,
            "hospital_id": self.hospital_id,
            "title": self.title,
            "details": self.details,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

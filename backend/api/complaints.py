from flask import Blueprint, request, jsonify
from sqlalchemy import or_
from sqlalchemy.orm import joinedload
from datetime import datetime
import math

from extensions import db
from models import Complaint, State, District, Hospital, User

api_complaints = Blueprint("api_complaints", __name__, url_prefix="/api/complaints")

def serialize_complaint_search(c):
        return {
            "complaint_id": c.complaint_id,
            "state_id": c.state_id,
            "district_id": c.district_id,
            "hospital_id": c.hospital_id,
            "title": c.title,
            "details": c.details,
            "created_at": getattr(c, "created_at", None).isoformat() if getattr(c, "created_at", None) else None,
            "state_name": getattr(c.state, "state_name", None) if hasattr(c, "state") else None,
            "district_name": getattr(c.district, "district_name", None) if hasattr(c, "district") else None,
            "hospital_name": getattr(c.hospital, "hospital_name", None) if hasattr(c, "hospital") else None,
        }

def serialize_complaint(complaint, state, district, hospital):
    return {
        "complaint_id": complaint.complaint_id,
        "name": complaint.name,
        "state_id": complaint.state_id,
        "district_id": complaint.district_id,
        "hospital_id": complaint.hospital_id,
        "title": complaint.title,
        "details": complaint.details,
        "created_at": complaint.created_at.isoformat() if complaint.created_at else None,
        "updated_at": complaint.updated_at.isoformat() if complaint.updated_at else None,
        "state": (
            {
                "state_id": state.state_id,
                "state_name": state.state_name,
                "latitude": state.latitude,
                "longitude": state.longitude,
            } if state else None
        ),
        "district": (
            {
                "district_id": district.district_id,
                "district_name": district.district_name,
                "latitude": district.latitude,
                "longitude": district.longitude,
            } if district else None
        ),
        "hospital": (
            {
                "hospital_id": hospital.hospital_id,
                "hospital_name": hospital.hospital_name,
                "address": hospital.address,
                "pincode": hospital.pincode,
                "latitude": hospital.latitude,
                "longitude": hospital.longitude,
                "total_beds": hospital.total_beds,
                "hospital_type": hospital.hospital_type,
                "government_subtype": hospital.government_subtype,
            } if hospital else None
        ),
    }

@api_complaints.route("/", methods=["POST"])
def create_complaint():
    """
    POST /api/complaints
    JSON:
    {
        "phone_number": "9876543210",
        "name": "Chaitanya",
        "state_id": 18,
        "district_id": 4,
        "hospital_id": 23,
        "title": "Overcharging",
        "details": "Hospital billed extra for basic facilities."
    }
    """
    data = request.get_json() or {}

    # Validate required fields
    required_fields = ["phone_number", "name", "title", "details", "state_id", "district_id", "hospital_id"]

    missing = [f for f in required_fields if not data.get(f)]
    if missing:
        return jsonify({"error": f"Missing required fields: {', '.join(missing)}"}), 400

    state_id = data.get("state_id")
    district_id = data.get("district_id")
    hospital_id = data.get("hospital_id")

    # Verify (state_id, hospital_id) pair exists
    hospital = Hospital.query.filter_by(state_id=state_id, hospital_id=hospital_id).first()
    if not hospital:
        return jsonify({
            "error": f"Invalid hospital_id={hospital_id} for state_id={state_id}. "
                     "No such hospital exists."
        }), 400

    # Verify district_id matches hospital record
    if hospital.district_id != district_id:
        return jsonify({
            "error": f"Hospital (id={hospital_id}) belongs to district_id={hospital.district_id}, but complaint has district_id={district_id}."
        }), 400

    # Create user if not exists
    user = User.query.filter_by(phone_number=data["phone_number"]).first()
    if not user:
        user = User(
            phone_number = data["phone_number"],
            name = data["name"],
            details = {"created_at": datetime.utcnow().isoformat()}
        )
        db.session.add(user)

    # Create Complaint
    complaint = Complaint(
        mobile = data["phone_number"],
        name = data["name"],
        state_id = state_id,
        district_id = district_id,
        hospital_id = hospital_id,
        title = data["title"],
        details = data["details"]
    )

    db.session.add(complaint)
    db.session.commit()

    return jsonify({
        "message": "Complaint created successfully",
        "data": complaint.to_dict()
    }), 201



@api_complaints.route("/", methods=["GET"])
def get_complaints():
    """
    Query params:
      state_id: int
      district_id: int
      hospital_id: int
      search: str   # matches title OR details (ILIKE %search%)
      page: int (default 1)
      page_size: int (default 20, max 100)
      order_by: str (default 'created_at' if present else 'complaint_id')
      order_dir: 'asc'|'desc' (default 'desc')
    """
    state_id = request.args.get("state_id", type=int)
    district_id = request.args.get("district_id", type=int)
    hospital_id = request.args.get("hospital_id", type=int)
    search = request.args.get("search", type=str)

    page = request.args.get("page", default=1, type=int)
    page_size = request.args.get("page_size", default=20, type=int)
    page_size = max(1, min(page_size or 20, 100))

    order_by = request.args.get("order_by", default=None, type=str)
    order_dir = request.args.get("order_dir", default="desc", type=str)

    query = (
        Complaint.query
        .options(
            joinedload(Complaint.state),
            joinedload(Complaint.district),
            joinedload(Complaint.hospital) if hasattr(Complaint, "hospital") else joinedload(Complaint.district)
        )
    )

    # Exact filters
    if state_id is not None:
        query = query.filter(Complaint.state_id == state_id)
    if district_id is not None:
        query = query.filter(Complaint.district_id == district_id)
    if hospital_id is not None:
        query = query.filter(Complaint.hospital_id == hospital_id)

    # Textbox search across title and details
    if search:
        like = f"%{search}%"
        query = query.filter(or_(
            Complaint.title.ilike(like),
            Complaint.details.ilike(like),
        ))

    # Ordering
    default_order_col = getattr(Complaint, "created_at", None) or Complaint.complaint_id
    order_col = getattr(Complaint, order_by) if (order_by and hasattr(Complaint, order_by)) else default_order_col
    query = query.order_by(order_col.asc() if order_dir.lower() == "asc" else order_col.desc())

    # Pagination
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()

    return jsonify({
        "data": [serialize_complaint_search(c) for c in items],
        "pagination": {
            "page": page,
            "page_size": page_size,
            "total": total,
            "total_pages": math.ceil(total / page_size),
            "has_next": page * page_size < total,
            "has_prev": page > 1,
        }
    })


# Get Complaint by ID
@api_complaints.route("/<int:complaint_id>", methods=["GET"])
def get_complaint(complaint_id):
    """
    GET /api/complaints/<complaint_id>
    Returns complaint details (without phone number) including state, district, and hospital info.
    """
    # Fetch complaint
    complaint = Complaint.query.get_or_404(complaint_id)

    # Fetch related data manually
    state = State.query.get(complaint.state_id) if complaint.state_id else None

    district = (
        District.query.filter_by(
            state_id = complaint.state_id if state else None,
            district_id = complaint.district_id
        ).first()
        if (complaint.state_id and complaint.district_id and state)
        else None
    )

    hospital = (
        Hospital.query.filter_by(
            hospital_id = complaint.hospital_id,
            state_id = complaint.state_id
        ).first()
        if (complaint.hospital_id and complaint.state_id)
        else None
    )

    # Build response (hide mobile)
    data = serialize_complaint(complaint, state, district, hospital)

    return jsonify({"data": data}), 200
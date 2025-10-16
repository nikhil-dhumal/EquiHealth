from flask import Blueprint, jsonify, request
from extensions import db
from models import State, District, Hospital
from sqlalchemy.orm import joinedload

api_hospitals = Blueprint("hospitals", __name__, url_prefix="/api/hospitals")


def serialize_hospital(h):
    """Serialize hospital with state, district, and categories."""
    return {
        **h.to_dict(),
        "state": (
            {
                "state_id": h.state.state_id,
                "state_name": h.state.state_name,
                "latitude": h.state.latitude,
                "longitude": h.state.longitude,
            } if h.state else None
        ),
        "district": (
            {
                "district_id": h.district.district_id,
                "district_name": h.district.district_name,
                "state_id": h.district.state_id,
                "latitude": h.district.latitude,
                "longitude": h.district.longitude,
            } if h.district else None
        ),
        "categories": [
            {"category_id": c.category_id, "category_name": c.category_name} for c in (h.categories or [])
        ],
    }


def fetch_hospitals(state_id, district_id=None, hospital_id=None):
    """Internal helper to fetch hospitals efficiently."""
    query = (
        Hospital.query
        .options(
            joinedload(Hospital.state),
            joinedload(Hospital.district),
            joinedload(Hospital.categories),
        )
        .filter_by(state_id=state_id)
    )
    if district_id:
        query = query.filter_by(district_id=district_id)

    if hospital_id:
        query = query.filter_by(hospital_id=hospital_id)

    return query.order_by(Hospital.hospital_name.asc()).all()


# get compact hospital by state_id, district_id and/or hospital_id
@api_hospitals.route("/compact", methods=["GET"])
def get_hospitals_compact():
    state_id = request.args.get("state_id", type=int)
    district_id = request.args.get("district_id", type=int)
    hospital_id = request.args.get("hospital_id", type=int)

    query = (
        Hospital.query
        .filter_by(state_id=state_id)
    )

    if district_id:
        query = query.filter_by(district_id=district_id)

    if hospital_id:
        query = query.filter_by(hospital_id=hospital_id)

    hospitals = query.order_by(Hospital.hospital_name.asc()).all()

    return jsonify({
        "count": len(hospitals),
        "data": [h.to_dict() for h in hospitals]
    }), 200


# Hospitals by State
@api_hospitals.route("/", methods=["GET"])
def get_hospitals():
    state_id = request.args.get("state_id", type=int) # defailt None
    district_id = request.args.get("district_id", type=int)
    hospital_id = request.args.get("hospital_id", type=int)

    hospitals = fetch_hospitals(state_id, district_id, hospital_id)

    if not hospitals:
        return jsonify({"message": f"No hospitals found for state_id {state_id}, district_id {district_id}, hospital_id {hospital_id}"}), 404

    data = [serialize_hospital(h) for h in hospitals]
    return jsonify({"count": len(data), "data": data}), 200


@api_hospitals.route("/grouped/", methods=["GET"])
def get_grouped_hospitals():
    """
    Return hospitals grouped by state → district → hospitals.
    Supports:
        /api/hospitals/grouped/<state_id>
        /api/hospitals/grouped/<state_id>/<district_id>
    """
    state_id = request.args.get("state_id", type=int) # defailt None
    district_id = request.args.get("district_id", type=int)

    # Efficient preloading of relationships
    query = (
        Hospital.query
        .options(
            joinedload(Hospital.state),
            joinedload(Hospital.district)
        )
        .filter(Hospital.state_id == state_id)
        .order_by(Hospital.district_id, Hospital.hospital_name)
    )

    if district_id is not None:
        query = query.filter(Hospital.district_id == district_id)

    hospitals = query.all()
    if not hospitals:
        msg = f"No hospitals found for state_id {state_id}"
        if district_id:
            msg += f", district_id {district_id}"
        return jsonify({"message": msg, "count": 0, "data": []}), 404

    # Build hierarchy: state → districts → hospitals
    state_map = {}

    for h in hospitals:
        if not h.state:
            continue

        state_id = h.state.state_id
        district_id_val = h.district.district_id if h.district else None

        # State
        if state_id not in state_map:
            state_map[state_id] = {
                "state_id": h.state.state_id,
                "state_name": h.state.state_name,
                "latitude": h.state.latitude,
                "longitude": h.state.longitude,
                "districts": {}
            }

        state_entry = state_map[state_id]

        # District
        if district_id_val and district_id_val not in state_entry["districts"]:
            state_entry["districts"][district_id_val] = {
                "district_id": h.district.district_id,
                "district_name": h.district.district_name,
                "hospitals": []
            }

        # Hospital
        hospital_data = {
            "hospital_id": h.hospital_id,
            "hospital_name": h.hospital_name,
            "address": h.address,
            "pincode": h.pincode,
            "latitude": h.latitude,
            "longitude": h.longitude,
            "total_beds": h.total_beds,
            "hospital_type": h.hospital_type,
            "government_subtype": h.government_subtype
        }

        if district_id_val:
            state_entry["districts"][district_id_val]["hospitals"].append(hospital_data)
            if state_entry["districts"][district_id_val].get("count", None):
                state_entry["districts"][district_id_val]["count"] += 1
            else:
                state_entry["districts"][district_id_val]["count"] = 1

    # Convert dicts to lists
    result = []
    for state in state_map.values():
        state["districts"] = list(state["districts"].values())
        state["count"] = len(state["districts"])
        result.append(state)

    return jsonify({"count": len(result), "data": result}), 200

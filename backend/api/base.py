from flask import Blueprint, jsonify, request
from sqlalchemy.orm import joinedload

from extensions import db
from models import State, District, Hospital

api_base = Blueprint("api", __name__, url_prefix="/api")

def serialize_district(d: District):
        return {
            **d.to_dict(),
            "state_name": d.state.state_name if d.state else None
        }

@api_base.route("/health", methods=["GET"])
def health():
    return jsonify({"ok": True, "status": "healthy"})

@api_base.route("/echo", methods=["POST"])
def echo():
    data = request.get_json(silent=True) or {}
    return jsonify({"ok": True, "you_sent": data})

# GET /api/states
# Retrieve a list of all states available in the system.
@api_base.route("/states", methods=["GET"])
def get_states():
    states = State.query.order_by(State.state_name.asc()).all()

    return jsonify({
        "count": len(states),
        "data": [s.to_dict() for s in states]
    }), 200

# GET /api/districts
# Retrieve districts either for a specific state or for all states.
# Query Parameters:
#   - state_id (int, optional): If provided, returns districts belonging
#     only to that state. If omitted, returns all districts across all states.
@api_base.route("/districts", methods=["GET"])
def get_districts():
    state_id = request.args.get("state_id", type=int)
    district_id = request.args.get("district_id", type=int)
    query = (
        District.query
        .options(
            joinedload(District.state),
        )
    )

    if state_id:
        query = query.filter_by(state_id=state_id)

    if district_id:
        query = query.filter_by(district_id=district_id)

    districts = query.order_by(District.state_id.asc(), District.district_id.asc()).all()

    if not districts:
        msg = "No districts found"
        if state_id is not None:
            msg += f" for state_id {state_id}"
        if district_id is not None:
            msg += f", district_id {district_id}"
        return jsonify({"message": msg, "count": 0, "data": []}), 404

    return jsonify({
        "count": len(districts),
        "data": [serialize_district(d) for d in districts],
    }), 200


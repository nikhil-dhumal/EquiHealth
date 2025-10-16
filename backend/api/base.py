from flask import Blueprint, jsonify, request
from extensions import db
from models import State, District, Hospital

api_base = Blueprint("api", __name__, url_prefix="/api")

@api_base.route("/health", methods=["GET"])
def health():
    return jsonify({"ok": True, "status": "healthy"})

@api_base.route("/echo", methods=["POST"])
def echo():
    data = request.get_json(silent=True) or {}
    return jsonify({"ok": True, "you_sent": data})

# --- All States ---
@api_base.route("/states", methods=["GET"])
def get_states():
    """Return list of all states."""
    states = State.query.order_by(State.state_name.asc()).all()
    return jsonify({
        "count": len(states),
        "data": [s.to_dict() for s in states]
    }), 200


# --- All Districts ---
@api_base.route("/districts", methods=["GET"])
def get_districts():
    """Return list of all districts."""
    state_id = request.args.get("state_id", type=int)
    if not state_id:
        districts = District.query.order_by(District.state_id.asc(), District.district_name.asc()).all()
    else:
        districts = District.query.filter_by(state_id=state_id).order_by(District.district_name.asc()).all()

    if not districts:
        return jsonify({"message": f"No districts found for state_id {state_id}"}), 404

    return jsonify({
        "count": len(districts),
        "data": [d.to_dict() for d in districts]
    }), 200


# --- Districts by State ID ---
# @api_base.route("/states/<int:state_id>/districts", methods=["GET"])
# def get_districts_by_state(state_id):
#     """Return all districts belonging to a given state."""
#     districts = District.query.filter_by(state_id=state_id).order_by(District.district_name.asc()).all()
#     if not districts:
#         return jsonify({"message": f"No districts found for state_id {state_id}"}), 404
#     return jsonify({
#         "count": len(districts),
#         "data": [d.to_dict() for d in districts]
#     }), 200


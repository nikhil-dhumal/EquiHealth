from flask import Blueprint, request, jsonify
from models import User

api_users = Blueprint("api_users", __name__, url_prefix="/api/users")

# GET /api/users?phone_number=9876543210
# Returns the user's name (and optional metadata) if found.
@api_users.route("/", methods=["GET"])
def get_user():
    phone_number = request.args.get("phone_number", type=str)

    if not phone_number:
        return jsonify({"error": "Missing required parameter: phone_number"}), 400

    user = User.query.filter_by(phone_number=phone_number).first()

    if not user:
        return jsonify({"message": f"No user found with phone number {phone_number}"}), 404

    return jsonify({
        "data": {
            "name": user.name,
            "phone_number": user.phone_number,
            "metadata": user.details or {}
        }
    }), 200

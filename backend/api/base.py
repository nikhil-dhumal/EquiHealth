from flask import Blueprint, jsonify, request

api_base = Blueprint("api", __name__, url_prefix="/api")

@api_base.route("/health", methods=["GET"])
def health():
    return jsonify({"ok": True, "status": "healthy"})

@api_base.route("/echo", methods=["POST"])
def echo():
    data = request.get_json(silent=True) or {}
    return jsonify({"ok": True, "you_sent": data})

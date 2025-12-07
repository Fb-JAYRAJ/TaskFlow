from flask import Blueprint, jsonify

api_v1_bp = Blueprint("api_v1", __name__)

@api_v1_bp.route("/health")
def health_check():
    return jsonify({"status": "ok", "version": "v1"})
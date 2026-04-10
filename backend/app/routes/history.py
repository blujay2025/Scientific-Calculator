from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app import db
from app.models import CalculationHistory

history_bp = Blueprint("history", __name__)


@history_bp.get("")
@jwt_required()
def list_history():
    user_id = int(get_jwt_identity())
    limit = min(int(request.args.get("limit", 50)), 100)
    rows = (
        CalculationHistory.query.filter_by(user_id=user_id)
        .order_by(CalculationHistory.created_at.desc())
        .limit(limit)
        .all()
    )
    return jsonify({"history": [row.to_dict() for row in rows]})


@history_bp.delete("/<int:history_id>")
@jwt_required()
def delete_history_item(history_id: int):
    user_id = int(get_jwt_identity())
    row = CalculationHistory.query.filter_by(id=history_id, user_id=user_id).first_or_404()
    db.session.delete(row)
    db.session.commit()
    return jsonify({"message": "History item deleted."})


@history_bp.delete("")
@jwt_required()
def clear_history():
    user_id = int(get_jwt_identity())
    CalculationHistory.query.filter_by(user_id=user_id).delete()
    db.session.commit()
    return jsonify({"message": "History cleared."})

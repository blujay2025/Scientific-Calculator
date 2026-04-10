from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app import db
from app.models import CalculationHistory
from app.services import evaluate_expression

calc_bp = Blueprint("calculator", __name__)


@calc_bp.post("/evaluate")
@jwt_required(optional=True)
def evaluate():
    data = request.get_json() or {}
    expression = data.get("expression") or ""
    angle_mode = (data.get("angle_mode") or "RAD").upper()
    ans = data.get("ans") or 0
    save_history = bool(data.get("save_history", True))

    try:
        result_payload = evaluate_expression(expression, angle_mode, ans)
    except ValueError as exc:
        return jsonify({"message": str(exc)}), 400

    user_id = get_jwt_identity()
    if user_id and save_history:
        history = CalculationHistory(
            user_id=int(user_id),
            expression=expression,
            normalized_expression=result_payload["normalized_expression"],
            result=result_payload["result"],
            angle_mode=angle_mode,
        )
        db.session.add(history)
        db.session.commit()

    return jsonify(result_payload)

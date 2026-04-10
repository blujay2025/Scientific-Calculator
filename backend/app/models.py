from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from . import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    calculations = db.relationship(
        "CalculationHistory", backref="user", lazy=True, cascade="all, delete-orphan"
    )

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.isoformat(),
        }


class CalculationHistory(db.Model):
    __tablename__ = "calculation_history"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    expression = db.Column(db.Text, nullable=False)
    normalized_expression = db.Column(db.Text, nullable=False)
    result = db.Column(db.String(255), nullable=False)
    angle_mode = db.Column(db.String(10), default="RAD", nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "expression": self.expression,
            "normalized_expression": self.normalized_expression,
            "result": self.result,
            "angle_mode": self.angle_mode,
            "created_at": self.created_at.isoformat(),
        }

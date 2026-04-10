import os
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

db = SQLAlchemy()
jwt = JWTManager()


def _get_allowed_origins():
    raw_origins = os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173,http://localhost:4173,http://127.0.0.1:4173,http://localhost:8080,http://127.0.0.1:8080",
    )
    return [origin.strip() for origin in raw_origins.split(",") if origin.strip()]


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "jwt-secret")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "mysql+pymysql://root:password@localhost:3306/scicalc_db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    allowed_origins = _get_allowed_origins()
    CORS(
        app,
        resources={r"/api/*": {"origins": allowed_origins}},
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "OPTIONS"],
        supports_credentials=False,
    )

    db.init_app(app)
    jwt.init_app(app)

    from .routes.auth import auth_bp
    from .routes.calc import calc_bp
    from .routes.history import history_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(calc_bp, url_prefix="/api/calculator")
    app.register_blueprint(history_bp, url_prefix="/api/history")

    @app.get("/api/health")
    def health_check():
        return jsonify({"status": "ok"})

    @app.errorhandler(Exception)
    def handle_exception(error):
        app.logger.exception("Unhandled exception: %s", error)
        return jsonify({"message": str(error)}), 500

    with app.app_context():
        from . import models
        db.create_all()

    return app

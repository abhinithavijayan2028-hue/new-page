import os
from flask import Flask, jsonify
from backend.config import DevelopmentConfig, TestingConfig, ProductionConfig
from backend.extensions import db, migrate, jwt, bcrypt, cors, talisman, limiter


def create_app(config_name=None):
    """Application factory pattern."""
    app = Flask(__name__)

    # Load configuration
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "development")

    config_map = {
        "development": DevelopmentConfig,
        "testing": TestingConfig,
        "production": ProductionConfig,
    }
    app.config.from_object(config_map.get(config_name, DevelopmentConfig))

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(app, origins=app.config.get("CORS_ORIGINS", []))
    talisman.init_app(app, force_https=app.config.get("FORCE_HTTPS", False))
    limiter.init_app(app)

    # Health check endpoint
    @app.route("/api/health", methods=["GET"])
    def health():
        return jsonify({
            "status": "success",
            "message": "NEXORITHAM backend is running",
            "environment": config_name,
        }), 200

    # Register blueprints (placeholder for future phases)
    # from routes.auth import auth_bp
    # app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")

    # Shell context for flask cli
    @app.shell_context_processor
    def make_shell_context():
        return {"db": db, "app": app}

    return app
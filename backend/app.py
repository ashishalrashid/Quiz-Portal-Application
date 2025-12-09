import os
from datetime import timedelta

from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_restful import Api

from models import db
from cache import init_cache
from config import Config
from routes import register_resources


def create_app():
    """Create and configure Flask application"""
    basedir = os.path.abspath(os.path.dirname(__file__))
    instance_path = os.path.abspath(os.path.join(basedir, "..", "instance"))

    app = Flask(__name__, instance_relative_config=True, instance_path=instance_path)

    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    # Configure CORS
    CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)

    # Load configuration
    app.config.from_mapping({
        **vars(Config),
        "SQLALCHEMY_DATABASE_URI": Config.get_db_uri(app.instance_path),
        "JWT_ACCESS_TOKEN_EXPIRES": Config.JWT_ACCESS_TOKEN_EXPIRES,
    })

    # Initialize extensions
    db.init_app(app)
    JWTManager(app)
    Limiter(app, key_func=get_remote_address, default_limits=["2000 per day", "500 per hour"])
    init_cache(app)

    # Create database tables
    with app.app_context():
        db.create_all()

    # Initialize API and register routes
    api = Api(app)
    register_resources(api)

    # JWT error handler
    jwt = JWTManager(app)

    @jwt.invalid_token_loader
    def invalid_token_callback(error_string):
        return jsonify({"msg": "Invalid token: " + error_string}), 422

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
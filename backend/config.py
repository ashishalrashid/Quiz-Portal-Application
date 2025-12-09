import os
from datetime import timedelta

class Config:
    """Base configuration"""
    CORS_HEADERS = ["Content-Type", "Authorization"]
    JWT_SECRET_KEY = "super-secret"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    @staticmethod
    def get_db_uri(instance_path):
        return "sqlite:///" + os.path.join(instance_path, "db.sqlite3")
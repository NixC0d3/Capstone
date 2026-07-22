import os
from dotenv import load_dotenv

load_dotenv()

class Config(object):
    """Base Config Object"""
    DEBUG = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "Som3$ec5etK*y")
    UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER", "uploads")

    # PostgreSQL example:
    # DATABASE_URL=postgresql://postgres:your_password@localhost:5432/capstone
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/capstone"
    ).replace("postgres://", "postgresql://")

    SQLALCHEMY_TRACK_MODIFICATIONS = False

import os

class Config:
    # Use PostgreSQL by default, fallback to SQLite for quick local testing if no URL is provided
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///students.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-prod')
    PORT = int(os.environ.get('PORT', 5000))
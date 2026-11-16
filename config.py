import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "chave-apenas-para-desenvolvimento")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{BASE_DIR / 'flasky.db'}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    BREVO_API_KEY = os.environ.get("BREVO_API_KEY", "").strip()
    BREVO_FROM = os.environ.get("BREVO_FROM", "").strip()
    STUDENT_EMAIL = os.environ.get("STUDENT_EMAIL", "").strip()
    PROFESSOR_EMAIL = "flaskaulasweb@zohomail.com"

    RESEND_API_KEY = os.environ.get("RESEND_API_KEY", "").strip()
    RESEND_FROM = os.environ.get("RESEND_FROM", "onboarding@resend.dev").strip()
    API_KEY = os.environ.get("API_KEY", "").strip()
    API_FROM = os.environ.get("API_FROM", "").strip()
    APP_BASE_URL = os.environ.get("APP_BASE_URL", "").rstrip("/")
    SESSION_COOKIE_SECURE = APP_BASE_URL.startswith("https://")
    REMEMBER_COOKIE_SECURE = SESSION_COOKIE_SECURE
    SESSION_COOKIE_SAMESITE = "Lax"
    CONFIRMATION_MAX_AGE = 86400

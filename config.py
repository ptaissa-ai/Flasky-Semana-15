import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "chave-apenas-para-desenvolvimento")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{BASE_DIR / 'flasky.db'}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # E-mail SMTP: configure estas variáveis no ambiente de hospedagem.
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", "587"))
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "true").lower() == "true"
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME", "")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", "")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER", "")
    MAIL_SUPPRESS_SEND = os.environ.get("MAIL_SUPPRESS_SEND", "false").lower() == "true"
    CONFIRMATION_MAX_AGE = int(os.environ.get("CONFIRMATION_MAX_AGE", "86400"))

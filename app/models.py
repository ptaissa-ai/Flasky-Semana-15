from datetime import datetime
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from flask_login import UserMixin
from app import db, login_manager

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="User")
    confirmed = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    @property
    def password(self):
        raise AttributeError("password não é um atributo legível.")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self):
        serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
        return serializer.dumps(self.id, salt="account-confirmation")

    def confirm(self, token):
        serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
        try:
            user_id = serializer.loads(
                token,
                salt="account-confirmation",
                max_age=current_app.config["CONFIRMATION_MAX_AGE"]
            )
        except (BadSignature, SignatureExpired):
            return False

        if user_id != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        return True

@login_manager.user_loader
def load_user(user_id):
    try:
        return db.session.get(User, int(user_id))
    except (TypeError, ValueError):
        return None

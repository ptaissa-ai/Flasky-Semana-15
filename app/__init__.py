import click
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
csrf = CSRFProtect()
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.login_message = "Faça login para acessar esta página."
login_manager.login_message_category = "warning"

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)

    from app import models
    from app.auth import auth as auth_blueprint
    from app.main import main as main_blueprint

    app.register_blueprint(auth_blueprint, url_prefix="/auth")
    app.register_blueprint(main_blueprint)

    with app.app_context():
        db.create_all()

    @app.cli.command("promover-admin")
    @click.argument("email")
    def promote_admin(email):
        """Promove uma conta confirmada a administradora."""
        user = db.session.scalar(db.select(models.User).filter_by(email=email.strip().lower()))
        if user is None or not user.confirmed:
            raise click.ClickException("Cadastre e confirme essa conta primeiro.")
        user.role = "Administrator"
        db.session.commit()
        click.echo("Conta promovida a administradora.")

    return app

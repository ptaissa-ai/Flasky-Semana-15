from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models import User

class LoginForm(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Length(1, 120), Email()])
    password = PasswordField("Senha", validators=[DataRequired()])
    remember_me = BooleanField("Manter conectado")
    submit = SubmitField("Entrar")

class RegistrationForm(FlaskForm):
    name = StringField("Nome completo", validators=[DataRequired(), Length(max=80)])
    username = StringField("Nome de usuário", validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField("E-mail", validators=[DataRequired(), Length(max=120), Email()])
    password = PasswordField("Senha", validators=[DataRequired(), Length(min=8)])
    password2 = PasswordField(
        "Confirme a senha",
        validators=[DataRequired(), EqualTo("password", message="As senhas precisam ser iguais.")]
    )
    submit = SubmitField("Criar conta")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError("Este e-mail já está cadastrado.")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Este nome de usuário já está em uso.")

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class UserForm(FlaskForm):
    name = StringField(
        "Nome",
        validators=[DataRequired(message="Informe o nome."), Length(max=80)]
    )
    email = StringField(
        "E-mail",
        validators=[DataRequired(message="Informe o e-mail."),
                    Email(message="Digite um e-mail válido."), Length(max=120)]
    )
    submit = SubmitField("Cadastrar usuário")

class EditUserForm(FlaskForm):
    name = StringField("Nome", validators=[DataRequired(), Length(max=80)])
    email = StringField("E-mail", validators=[DataRequired(), Email(), Length(max=120)])
    submit = SubmitField("Salvar")

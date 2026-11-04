from flask import render_template, redirect, url_for, flash, session
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError
from app import db
from app.models import User
from app.main import main

@main.route("/")
def index():
    users = User.query.order_by(User.id.desc()).all() if current_user.is_authenticated and current_user.confirmed else []
    return render_template("index.html", users=users)

@main.route("/editar/<int:user_id>", methods=["GET", "POST"])
@login_required
def edit_user(user_id):
    if not current_user.confirmed:
        return redirect(url_for("auth.unconfirmed"))
    user = User.query.get_or_404(user_id)
    # Formulário simples reaproveitando os campos de cadastro, sem alterar senha.
    from flask_wtf import FlaskForm
    from wtforms import StringField, SubmitField
    from wtforms.validators import DataRequired, Email, Length
    class EditForm(FlaskForm):
        name = StringField("Nome completo", validators=[DataRequired(), Length(max=80)])
        email = StringField("E-mail", validators=[DataRequired(), Email(), Length(max=120)])
        username = StringField("Nome de usuário", validators=[DataRequired(), Length(min=3, max=64)])
        submit = SubmitField("Salvar alterações")
    form = EditForm()
    if form.validate_on_submit():
        user.name = form.name.data.strip()
        user.email = form.email.data.lower().strip()
        user.username = form.username.data.strip()
        try:
            db.session.commit()
            flash("Usuário atualizado.", "success")
            return redirect(url_for("main.index"))
        except IntegrityError:
            db.session.rollback()
            flash("E-mail ou nome de usuário já utilizado por outra conta.", "danger")
    elif not form.is_submitted():
        form.name.data, form.email.data, form.username.data = user.name, user.email, user.username
    return render_template("edit.html", form=form, user=user)

@main.post("/excluir/<int:user_id>")
@login_required
def delete_user(user_id):
    if not current_user.confirmed:
        return redirect(url_for("auth.unconfirmed"))
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash("Você não pode excluir a própria conta enquanto estiver conectado.", "warning")
        return redirect(url_for("main.index"))
    db.session.delete(user)
    db.session.commit()
    flash("Usuário excluído.", "success")
    return redirect(url_for("main.index"))

@main.get("/health")
def health():
    return {"status": "ok"}

from flask import render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy.exc import IntegrityError
from app import db
from app.models import User
from app.auth import auth
from app.auth.forms import LoginForm, RegistrationForm
from app.email_service import send_confirmation_email

@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower().strip()).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            confirmation_token = session.pop("pending_confirmation", None)
            if not user.confirmed and confirmation_token:
                return redirect(url_for("auth.confirm", token=confirmation_token))
            if not user.confirmed:
                return redirect(url_for("auth.unconfirmed"))
            flash("Login realizado com sucesso.", "success")
            return redirect(url_for("main.index"))
        flash("E-mail ou senha inválidos.", "danger")
    return render_template("auth/login.html", form=form)

@auth.post("/logout")
@login_required
def logout():
    logout_user()
    flash("Você saiu da sua conta.", "success")
    return redirect(url_for("main.index"))

@auth.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            name=form.name.data.strip(),
            username=form.username.data.strip(),
            email=form.email.data.lower().strip()
        )
        user.password = form.password.data
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            flash("E-mail ou nome de usuário já cadastrado.", "danger")
            return render_template("auth/register.html", form=form)

        sent = send_confirmation_email(user)
        if sent:
            flash("Cadastro realizado! Confira seu e-mail para confirmar a conta.", "success")
        else:
            flash("Cadastro realizado, mas o e-mail não foi enviado. Entre na conta e solicite novo envio.", "warning")
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html", form=form)

@auth.route("/confirm/<token>", methods=["GET", "POST"])
def confirm(token):
    if not current_user.is_authenticated:
        session["pending_confirmation"] = token
        flash("Entre para confirmar sua conta.", "info")
        return redirect(url_for("auth.login"))
    if current_user.confirmed:
        flash("Sua conta já está confirmada.", "info")
        return redirect(url_for("main.index"))
    if request.method == "GET":
        return render_template("auth/confirm.html")
    if current_user.confirm(token):
        flash("Conta confirmada com sucesso!", "success")
    else:
        flash("O link de confirmação é inválido ou expirou.", "danger")
    return redirect(url_for("main.index") if current_user.confirmed else url_for("auth.unconfirmed"))

@auth.route("/unconfirmed")
@login_required
def unconfirmed():
    if current_user.confirmed:
        return redirect(url_for("main.index"))
    return render_template("auth/unconfirmed.html")

@auth.post("/confirm")
@login_required
def resend_confirmation():
    if current_user.confirmed:
        return redirect(url_for("main.index"))
    if send_confirmation_email(current_user):
        flash("Um novo e-mail de confirmação foi enviado.", "success")
    else:
        flash("Não foi possível enviar o e-mail. Tente novamente mais tarde.", "warning")
    return redirect(url_for("auth.unconfirmed"))

@auth.before_app_request
def before_request():
    if (current_user.is_authenticated
            and not current_user.confirmed
            and request.blueprint != "auth"
            and request.endpoint != "static"):
        return redirect(url_for("auth.unconfirmed"))

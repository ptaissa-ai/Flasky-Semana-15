from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from sqlalchemy.exc import IntegrityError
from app import db
from app.models import User
from app.forms import UserForm, EditUserForm
from app.email_service import notify_admin

main = Blueprint("main", __name__)

@main.route("/", methods=["GET", "POST"])
def index():
    form = UserForm()
    if form.validate_on_submit():
        user = User(name=form.name.data.strip(), email=form.email.data.strip().lower())
        db.session.add(user)
        try:
            db.session.commit()
            session["visitor_name"] = user.name
            sent = notify_admin(user)
            if sent:
                flash("Usuário cadastrado e notificação enviada ao administrador.", "success")
            else:
                flash("Usuário cadastrado. O envio de e-mail não está configurado ou falhou.", "warning")
            return redirect(url_for("main.index"))
        except IntegrityError:
            db.session.rollback()
            flash("Este e-mail já está cadastrado.", "danger")

    users = User.query.order_by(User.id.desc()).all()
    return render_template("index.html", form=form, users=users,
                           visitor_name=session.get("visitor_name", "Desconhecido"))

@main.route("/editar/<int:user_id>", methods=["GET", "POST"])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = EditUserForm(obj=user)
    if form.validate_on_submit():
        user.name = form.name.data.strip()
        user.email = form.email.data.strip().lower()
        try:
            db.session.commit()
            flash("Dados do usuário atualizados.", "success")
            return redirect(url_for("main.index"))
        except IntegrityError:
            db.session.rollback()
            flash("Esse e-mail já pertence a outro usuário.", "danger")
    return render_template("edit.html", form=form, user=user)

@main.post("/excluir/<int:user_id>")
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash("Usuário excluído.", "success")
    return redirect(url_for("main.index"))

@main.get("/health")
def health():
    return {"status": "ok"}

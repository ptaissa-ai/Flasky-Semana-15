import requests
from flask import current_app, render_template, url_for


def send_confirmation_email(user):
    cfg = current_app.config
    if not cfg["API_KEY"] or not cfg["API_FROM"]:
        current_app.logger.warning("Configure API_KEY e API_FROM para enviar confirmações.")
        return False

    token = user.generate_confirmation_token()
    path = url_for("auth.confirm", token=token)
    base = cfg["APP_BASE_URL"]
    confirm_url = base + path if base else url_for(
        "auth.confirm", token=token, _external=True
    )
    context = {"user": user, "confirm_url": confirm_url}
    payload = {
        "personalizations": [{"to": [{"email": user.email}]}],
        "from": {"email": cfg["API_FROM"], "name": "Flasky — Semana 15"},
        "subject": "Confirme sua conta Flasky",
        "content": [
            {"type": "text/plain", "value": render_template("auth/email/confirm.txt", **context)},
            {"type": "text/html", "value": render_template("auth/email/confirm.html", **context)},
        ],
    }
    try:
        response = requests.post(
            "https://api.sendgrid.com/v3/mail/send",
            headers={"Authorization": "Bearer " + cfg["API_KEY"]},
            json=payload, timeout=15,
        )
    except requests.RequestException:
        current_app.logger.warning("Falha de comunicação com SendGrid.")
        return False
    if response.status_code != 202:
        current_app.logger.warning("SendGrid recusou a confirmação (HTTP %s).", response.status_code)
        return False
    return True

import requests
from flask import current_app, render_template, url_for


def send_confirmation_email(user):
    return send_account_email(user, "Confirme sua conta Flasky", "confirm",
                              "auth.confirm", user.generate_confirmation_token())


def send_password_reset_email(user, token):
    return send_account_email(user, "Redefina sua senha Flasky", "reset",
                              "auth.reset_password", token)


def send_account_email(user, subject, template, endpoint, token):
    cfg = current_app.config
    if not cfg["API_KEY"] or not cfg["API_FROM"]:
        current_app.logger.warning("Configure API_KEY e API_FROM para enviar e-mails.")
        return False

    base = cfg["APP_BASE_URL"]
    link = base + url_for(endpoint, token=token) if base else url_for(
        endpoint, token=token, _external=True
    )
    context = {"user": user, "confirm_url": link, "reset_url": link}
    payload = {
        "personalizations": [{"to": [{"email": user.email}]}],
        "from": {"email": cfg["API_FROM"], "name": "Flasky — Semana 15"},
        "subject": subject,
        "content": [
            {"type": "text/plain", "value": render_template(f"auth/email/{template}.txt", **context)},
            {"type": "text/html", "value": render_template(f"auth/email/{template}.html", **context)},
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
        current_app.logger.warning("SendGrid recusou o e-mail (HTTP %s).", response.status_code)
        return False
    return True

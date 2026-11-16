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
    resend_key = cfg["RESEND_API_KEY"]
    if not resend_key and (not cfg["API_KEY"] or not cfg["API_FROM"]):
        current_app.logger.warning("Configure API_KEY e API_FROM para enviar e-mails.")
        return False

    base = cfg["APP_BASE_URL"]
    link = base + url_for(endpoint, token=token) if base else url_for(
        endpoint, token=token, _external=True
    )
    context = {"user": user, "confirm_url": link, "reset_url": link}
    plain = render_template(f"auth/email/{template}.txt", **context)
    html = render_template(f"auth/email/{template}.html", **context)
    if resend_key:
        provider, url, key, status = "Resend", "https://api.resend.com/emails", resend_key, 200
        payload = {"from": cfg["RESEND_FROM"], "to": [user.email],
                   "subject": subject, "text": plain, "html": html}
    else:
        provider, url, key, status = "SendGrid", "https://api.sendgrid.com/v3/mail/send", cfg["API_KEY"], 202
        payload = {
            "personalizations": [{"to": [{"email": user.email}]}],
            "from": {"email": cfg["API_FROM"], "name": "Flasky — Semana 16"},
            "subject": subject,
            "content": [{"type": "text/plain", "value": plain},
                        {"type": "text/html", "value": html}],
        }
    try:
        response = requests.post(
            url,
            headers={"Authorization": "Bearer " + key},
            json=payload, timeout=15,
        )
    except requests.RequestException:
        current_app.logger.warning("Falha de comunicação com %s.", provider)
        return False
    if response.status_code != status:
        current_app.logger.warning("%s recusou o e-mail (HTTP %s).", provider, response.status_code)
        return False
    return True

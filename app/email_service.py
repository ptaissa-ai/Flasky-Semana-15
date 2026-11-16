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
    base = cfg["APP_BASE_URL"]
    link = base + url_for(endpoint, token=token) if base else url_for(
        endpoint, token=token, _external=True
    )
    context = {"user": user, "confirm_url": link, "reset_url": link}
    plain = render_template(f"auth/email/{template}.txt", **context)
    html = render_template(f"auth/email/{template}.html", **context)
    return send_message([user.email], subject, plain, html)


def send_registration_notice(user):
    cfg = current_app.config
    if not cfg["STUDENT_EMAIL"]:
        current_app.logger.warning("Preencha STUDENT_EMAIL para ativar os avisos acadêmicos.")
        return False
    subject = "Flasky — Semana 16: novo cadastro"
    body = (f"Aluna: Taissa Pieri\nProntuário: PT3038084\n"
            f"Usuário cadastrado: {user.username}\n")
    recipients = dict.fromkeys([cfg["STUDENT_EMAIL"].lower(), cfg["PROFESSOR_EMAIL"]])
    results = [send_message([email], subject, body) for email in recipients]
    return all(results)


def send_message(recipients, subject, plain, html=None):
    cfg = current_app.config
    addresses = [{"email": email} for email in recipients]
    if cfg["BREVO_API_KEY"]:
        if not cfg["BREVO_FROM"]:
            current_app.logger.warning("Preencha BREVO_FROM com o remetente verificado.")
            return False
        provider, url, status = "Brevo", "https://api.brevo.com/v3/smtp/email", 201
        headers = {"api-key": cfg["BREVO_API_KEY"]}
        payload = {"sender": {"email": cfg["BREVO_FROM"], "name": "Flasky"},
                   "to": addresses, "subject": subject, "textContent": plain}
        if html:
            payload["htmlContent"] = html
    elif cfg["RESEND_API_KEY"]:
        provider, url, status = "Resend", "https://api.resend.com/emails", 200
        headers = {"Authorization": "Bearer " + cfg["RESEND_API_KEY"]}
        payload = {"from": cfg["RESEND_FROM"], "to": recipients,
                   "subject": subject, "text": plain}
        if html:
            payload["html"] = html
    else:
        if not cfg["API_KEY"] or not cfg["API_FROM"]:
            current_app.logger.warning("Configure API_KEY e API_FROM para enviar e-mails.")
            return False
        provider, url, status = "SendGrid", "https://api.sendgrid.com/v3/mail/send", 202
        headers = {"Authorization": "Bearer " + cfg["API_KEY"]}
        payload = {
            "personalizations": [{"to": addresses}],
            "from": {"email": cfg["API_FROM"], "name": "Flasky — Semana 16"},
            "subject": subject,
            "content": [{"type": "text/plain", "value": plain}],
        }
        if html:
            payload["content"].append({"type": "text/html", "value": html})
    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload, timeout=15,
        )
    except requests.RequestException:
        current_app.logger.warning("Falha de comunicação com %s.", provider)
        return False
    if response.status_code != status:
        current_app.logger.warning("%s recusou o e-mail (HTTP %s).", provider, response.status_code)
        return False
    return True

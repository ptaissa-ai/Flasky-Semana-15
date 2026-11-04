import smtplib
from email.message import EmailMessage
from flask import current_app, render_template, url_for

def send_email(to, subject, template, **kwargs):
    cfg = current_app.config
    if cfg.get("MAIL_SUPPRESS_SEND"):
        current_app.logger.info("Envio de e-mail suprimido: %s", subject)
        return False

    required = [cfg.get("MAIL_SERVER"), cfg.get("MAIL_USERNAME"),
                cfg.get("MAIL_PASSWORD"), cfg.get("MAIL_DEFAULT_SENDER") or cfg.get("MAIL_USERNAME")]
    if not all(required):
        current_app.logger.warning(
            "SMTP não configurado. Configure MAIL_SERVER, MAIL_USERNAME, "
            "MAIL_PASSWORD e MAIL_DEFAULT_SENDER."
        )
        return False

    message = EmailMessage()
    message["Subject"] = subject
    message["From"] = cfg.get("MAIL_DEFAULT_SENDER") or cfg["MAIL_USERNAME"]
    message["To"] = to
    message.set_content(render_template(template + ".txt", **kwargs))
    message.add_alternative(render_template(template + ".html", **kwargs), subtype="html")

    try:
        with smtplib.SMTP(cfg["MAIL_SERVER"], cfg["MAIL_PORT"], timeout=20) as server:
            if cfg.get("MAIL_USE_TLS"):
                server.starttls()
            server.login(cfg["MAIL_USERNAME"], cfg["MAIL_PASSWORD"])
            server.send_message(message)
        return True
    except Exception:
        current_app.logger.exception("Não foi possível enviar o e-mail.")
        return False

def send_confirmation_email(user):
    token = user.generate_confirmation_token()
    confirm_url = url_for("auth.confirm", token=token, _external=True)
    return send_email(
        user.email,
        "Confirme sua conta Flasky",
        "auth/email/confirm",
        user=user,
        confirm_url=confirm_url
    )

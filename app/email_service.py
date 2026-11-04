import smtplib
from email.message import EmailMessage
from flask import current_app

def notify_admin(user):
    """Envia aviso por SMTP se as credenciais estiverem configuradas."""
    cfg = current_app.config
    required = [
        cfg.get("MAIL_SERVER"), cfg.get("MAIL_USERNAME"),
        cfg.get("MAIL_PASSWORD"), cfg.get("ADMIN_EMAIL")
    ]
    if not all(required):
        current_app.logger.info(
            "E-mail não enviado: configure MAIL_SERVER, MAIL_USERNAME, "
            "MAIL_PASSWORD e ADMIN_EMAIL nas variáveis de ambiente."
        )
        return False

    message = EmailMessage()
    message["Subject"] = "Novo usuário cadastrado no Flasky"
    message["From"] = cfg.get("MAIL_DEFAULT_SENDER") or cfg["MAIL_USERNAME"]
    message["To"] = cfg["ADMIN_EMAIL"]
    message.set_content(
        f"Um novo usuário foi cadastrado.\n\nNome: {user.name}\nE-mail: {user.email}"
    )

    try:
        with smtplib.SMTP(cfg["MAIL_SERVER"], cfg["MAIL_PORT"], timeout=15) as server:
            if cfg.get("MAIL_USE_TLS"):
                server.starttls()
            server.login(cfg["MAIL_USERNAME"], cfg["MAIL_PASSWORD"])
            server.send_message(message)
        return True
    except Exception:
        current_app.logger.exception("Falha ao enviar notificação por e-mail.")
        return False

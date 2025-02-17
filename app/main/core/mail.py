import smtplib
import logging
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Template
from app.main.core.config import Config

def send_account_creation_email(email_to: str, first_name: str, last_name: str, password: str) -> None:
    try:
        # Charger et rendre le template HTML
        template_path = Path(Config.EMAIL_TEMPLATES_DIR) / "account_creation.html"
        html_content = Template(template_path.read_text(encoding="utf-8")).render(
            first_name=first_name, last_name=last_name, password=password, project_name=Config.PROJECT_NAME
        )

        # Création et envoi de l'email
        msg = MIMEMultipart()
        msg["From"], msg["To"], msg["Subject"] = Config.EMAILS_FROM_CLOUDINARY, email_to, "API_ERP | Compte créé"
        msg.attach(MIMEText(html_content, "html"))

        with smtplib.SMTP(Config.MAILTRAP_HOST, Config.MAILTRAP_PORT) as server:
            server.starttls()
            server.login(Config.MAILTRAP_USERNAME, Config.MAILTRAP_PASSWORD)
            server.send_message(msg)

        logging.info(f"Email envoyé à {email_to}")

    except Exception as e:
        logging.error(f"Erreur envoi email : {e}")

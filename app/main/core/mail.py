import logging
import os
from email.message import EmailMessage
import smtplib
from email.utils import formataddr
from fastapi import HTTPException, Path
from typing import Any, Dict, List

from fastapi.templating import Jinja2Templates
from app.main.core.config import Config
# Configurations de Mailtrap (ajuste avec tes informations)
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email_validator import validate_email, EmailNotValidError

from app.main.core.i18n import get_language



# @celery.task(name="send_email")
# def send_email(
#         email_to: str,
#         subject_template: str = "",
#         html_template: str = "",
#         environment: Dict[str, Any] = {},
#         file: Any = []
# ) -> None:
#     assert Config.EMAILS_ENABLED, "aucune configuration fournie pour les variables de messagerie"
#     message = emails.Message(
#         subject=Jinja2Templates(subject_template),
#         html=Jinja2Templates(html_template),
#         mail_from=(Config.EMAILS_FROM_NAME, Config.EMAILS_FROM_EMAIL)
#     )
#     for attachment in file:
#         message.attach(data=open(attachment, 'rb'), filename=attachment.split("/")[-1])

#     smtp_options = {"host": Config.SMTP_HOST, "port": Config.SMTP_PORT}
#     if Config.SMTP_TLS:
#         smtp_options["tls"] = Config.SMTP_TLS
#     if Config.SMTP_SSL:
#         smtp_options["ssl"] = Config.SMTP_SSL
#     if Config.SMTP_USER:
#         smtp_options["user"] = Config.SMTP_USER
#     if Config.SMTP_PASSWORD:
#         smtp_options["password"] = Config.SMTP_PASSWORD
#     response = message.send(to=email_to, render=environment, smtp=smtp_options)
#     logging.info(f"résultat de l'email envoyé: {response}")


# def send_account_creation_email(email_to,prefered_language:str,first_name:str,last_name:str,password:str)->None:
#     project_name = Config.PROJECT_NAME
#     if str(prefered_language) in ["en","EN","en-EN"]:
#         subject = f"API_ERP | Account created succesfully"
#         content = "is your password. You must change it after the first connection for the better security"
#         with open(Path(Config.EMAIL_TEMPLATES_DIR)/ "account_creation.html") as f:
#             template_str = f.read()
#     else:
#         subject = f"API_ERP | Compte crée avec succès"
#         content = "est votre mot de passe.Vous avez l'obligation de le modifier aprės la première connexion pour une meilleure sécurité."

#         with open(Path(Config.EMAIL_TEMPLATES_DIR) / "account_creation.html") as f:
#             template_str = f.read()
#      task = send_email(
#         email_to=email_to,
#         subject_template=subject,
#         html_template=template_str,
#         environment={
#             "content": content,
#             "project_name": project_name,
#             "password": password,
#             "name": first_name,
#             "email": email_to
#         },
#     )

# def get_template_path_based_on_lang():
#     lang = get_language()
#     if lang not in ["en", "fr"]:
#         lang = "fr"
#     return f"{Config.EMAIL_TEMPLATES_DIR}/{lang}"





import smtplib
import jinja2
from flask import Flask, render_template_string
from flask_mail import Mail, Message

EMAIL_RENDERING_ERROR = "El renderizado del template para el body falló."
EMAIL_SMTP_ERROR = "El envío del mail falló."

class MailServiceError(Exception):
    """Custom exception for MailService errors."""
    pass

class MailService:
    """Service to send emails."""

    _mail: Mail

    @classmethod
    def init_app(cls, app: Flask) -> None:
        cls._mail = Mail()
        cls._mail.init_app(app)

    @classmethod
    def send_mail(
        cls,
        subject: str,
        recipients: str,
        body: str,
    ) -> None:
        """Send an email.

        Args:
            subject (str): The subject of the email.
            recipients (str): The email address of the recipient.
            body (str): The body of the email.
        """

        try:
            html = render_template_string(body)
        except jinja2.TemplateError as e:
            raise MailServiceError(e.message or EMAIL_RENDERING_ERROR)
        
        msg = Message(
            subject=subject,
            recipients=[recipients],
            html=html,
        )
        
        try:
            cls._mail.send(msg)
        except smtplib.SMTPException as e:
            raise MailServiceError(e.strerror or EMAIL_SMTP_ERROR)

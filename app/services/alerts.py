from twilio.rest import Client
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.core.config import settings

twilio_client = Client(settings.twilio_account_sid, settings.twilio_auth_token)

conf = ConnectionConfig(
    MAIL_USERNAME=settings.smtp_user,
    MAIL_PASSWORD=settings.smtp_pass,
    MAIL_FROM=settings.smtp_user,
    MAIL_PORT=settings.smtp_port,
    MAIL_SERVER=settings.smtp_host,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
)

def send_alerts(results):
    # SMS
    body = "\n".join([f"{r['ticker']} @ {r['price']}  vol {r['volume']}  {r['reason']}" for r in results])
    for num in settings.sms_recipients:
        twilio_client.messages.create(to=num, from_=settings.twilio_from, body=body)
    # Email
    html = "<h3>Breakout Alerts</h3><ul>" + "".join([f"<li>{r['ticker']} @ {r['price']}  vol {r['volume']}  {r['reason']}</li>" for r in results]) + "</ul>"
    message = MessageSchema(subject="Breakout Alerts", recipients=settings.email_recipients, body=html, subtype="html")
    fm = FastMail(conf)
    fm.send_message(message)

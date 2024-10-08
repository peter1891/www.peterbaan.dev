class MailMsg:

    def __init__(self, name: str, email: str, subject: str, message: str):
        self.name = name
        self.email = email
        self.subject = subject
        self.message = message

from dotenv import load_dotenv
import os

load_dotenv()

FROM_EMAIL_ADDRESS = os.getenv("SMTP_FROM_EMAIL")
TO_EMAIL_ADDRESS = os.getenv("SMTP_TO_EMAIL")
PASSWORD = os.getenv("SMTP_PASSOWRD")

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_msg(msg_content: MailMsg):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Nieuw Bericht van PeterBaan.dev"
    msg["From"] = FROM_EMAIL_ADDRESS
    msg["To"] = TO_EMAIL_ADDRESS

    plain = f"Naam: {msg_content.name}\nEmail: {msg_content.email}\nOnderwerp: {msg_content.subject}\nBericht: {msg_content.message}"
    html = f"""\
    <html>
        <head></head>
        <body>
            <p>Naam: {msg_content.name}</p>
            <p>Email: {msg_content.email}</p>
            <p>Onderwerp: {msg_content.subject}</p>
            <p>Bericht: {msg_content.message}</p>
        </body
    </html>
    """

    msg.attach(MIMEText(plain, "plain"))
    msg.attach(MIMEText(html, "html"))
    
    with smtplib.SMTP("smtp.strato.com", port=587) as connection:
        connection.ehlo()
        connection.starttls()
        connection.ehlo()
        connection.login(user=FROM_EMAIL_ADDRESS, password=PASSWORD)
        connection.sendmail(
            from_addr=FROM_EMAIL_ADDRESS, 
            to_addrs=TO_EMAIL_ADDRESS, 
            msg=msg.as_string()
            )
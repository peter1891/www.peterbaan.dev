from dotenv import load_dotenv
import smtplib
import os

load_dotenv()

FROM_EMAIL_ADDRESS = os.getenv("SMTP_FROM_EMAIL")
TO_EMAIL_ADDRESS = os.getenv("SMTP_TO_EMAIL")
PASSWORD = os.getenv("SMTP_PASSOWRD")

def send_msg(msg):
    with smtplib.SMTP("smtp.strato.com", port=587) as connection:
        connection.starttls()
        connection.login(user=FROM_EMAIL_ADDRESS, password=PASSWORD)
        connection.sendmail(
            from_addr=FROM_EMAIL_ADDRESS, 
            to_addrs=TO_EMAIL_ADDRESS, 
            msg=f"Subject:Nieuw Bericht van PeterBaan.dev\n\n{msg}"
            )
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from jinja2 import Template

SMTP_local_HOST="localhost"
SMTP_SERVER_PORT= 1025
SMTP_local_PORT= 1025
SENDER_ADDRESS = "sanjeevanimangla09@gmail.com"

def send_email(to_address, subject, message, attachment=None, attachment_name=None ):
    msg=MIMEMultipart()
    msg["From"] = SENDER_ADDRESS
    msg["To"] = to_address
    msg["Subject"] = subject

    if attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment)
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={attachment_name}")
        msg.attach(part)

    if message:
        msg.attach(MIMEText(message, "html"))
    
    k = smtplib.SMTP(host=SMTP_local_HOST, port=SMTP_local_PORT)
    k.login(SENDER_ADDRESS,"")
    k.send_message(msg)
    k.quit()

    return True 
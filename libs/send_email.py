import json
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime


def send_email(recipient, sender, passwd, subject, text, data):
    msg = MIMEMultipart('alternative')
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = subject

    body = text
    msg.attach(MIMEText(body, 'plain'))

    attachment = MIMEText(json.dumps(data))
    attachment.add_header('Content-Disposition', 'attachment', 
                          filename="multas.json")
    msg.attach(attachment)

    server = smtplib.SMTP('smtp-mail.outlook.com', 587)
    server.starttls()
    server.login(sender, passwd)
    server.send_message(msg)
    server.quit()

    return 0

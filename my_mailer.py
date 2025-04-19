from email.mime.text import MIMEText
from dotenv import load_dotenv

import smtplib, os


def send_mail(df):
    load_dotenv()
    recipient = os.getenv("RECIPIENT")
    subject = "Your Item List"
    sender = os.getenv("SENDER")
    password = os.getenv("MY_KEY")
    smtp_server = "smtp.gmail.com"
    smtp_port = 465  # Gmail SSL
    send_list_email(recipient, subject, df, sender, password, smtp_server, smtp_port)


def send_list_email(recipient_email, subject, df, sender_email, sender_password, smtp_server, smtp_port):
    if df.empty:
        print("Nothing new today, no mail")
    else:
        body = "New Blu-Rays:\n\n"

        for index, row in df.iterrows():
            body += row['name'] + "-" + row['price'] + "\n"

        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = recipient_email

        try:
            with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, [recipient_email], msg.as_string())
            print("Email sent successfully!")
        except Exception as e:
            print(f"Error sending email: {e}")

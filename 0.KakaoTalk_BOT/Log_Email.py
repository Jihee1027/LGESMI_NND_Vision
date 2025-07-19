import smtplib
from email.message import EmailMessage
from datetime import datetime

def email_setup(sender, password, recipient, subject, body):
    msg = EmailMessage()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.set_content(body)

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender, password)
            smtp.send_message(msg)
        print("Email sent successfully.")
    except Exception as e:
        print("Error sending email:", e)


def send_email_success(chatroom):
    email_setup(
        sender = "alice1027k@gmail.com",
        password = "cnka qnvi ejqw awdv",
        recipient = "kimjiheelgensol@gmail.com",
        subject = "Success!",
        body = "Success sending on " + chatroom + " at " + str(datetime.now())
    )

def send_email_fail(chatroom):
    email_setup(
        sender = "alice1027k@gmail.com",
        password = "cnka qnvi ejqw awdv",
        recipient = "kimjiheelgensol@gmail.com",
        subject = "FAIL PLEASE CHECK THE PROGRAM",
        body = "Fail sending on " + chatroom + " at " + str(datetime.now())
    )

def send_email_error(chatroom):
    email_setup(
        ssender = "alice1027k@gmail.com",
        password = "cnka qnvi ejqw awdv",
        recipient = "kimjiheelgensol@gmail.com",
        subject = "ERROR OCCUR",
        body = "ERROR" + chatroom + " at " + str(datetime.now())
    )
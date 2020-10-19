#!/usr/bin/python3
# Author:   @BlankGodd_

import csv
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from getpass import getpass

port = 465
smtp_server = "smtp.gmail.com"


def send_bulk_mail():
    sender_email = input("Enter Your email: ")
    print("Input password")
    password = getpass()

    subject = input('Enter email subject: ')

    # read text file
    with open("email.txt") as e_txt:
        text = e_txt.read()

    try:
        # read html file
        with open("email.html") as e_html:
            html = e_html.read()
    except:
        pass

    # open subscribers file
    with open("subscribers.csv") as file:
        item = csv.reader(file)
        next(item)  # Skip header row
        for name, receiver_email in item:

            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = sender_email
            message["To"] = receiver_email

            this_text = text.format(name)
            try:
                this_html = html.format(name)
            except:
                pass

            part1 = MIMEText(this_text, "plain")
            try:
                part2 = MIMEText(this_html, "html")
            except:
                pass

            message.attach(part1)
            try:
                message.attach(part2)
            except:
                pass

            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                server.login(sender_email, password)
                server.sendmail(
                    sender_email, receiver_email, message.as_string()
                )

            print(f"Sending email to {name}")


if __name__ == "__main__":
    send_bulk_mail()

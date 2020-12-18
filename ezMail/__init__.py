"""
Copyright <2020> <Jirapong Pansak>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from secrets import compare_digest
import re
import getpass

class RequiredFieldEmptyError(Exception):
    pass


class InvalidMailServerError(Exception):
    pass


class EmailSender:
    # initialise the Multipart message
    def __init__(self):
        self.mail_package = MIMEMultipart("alternative")
        # set fields to empty
        self.sender_mail = ""
        self.receiver_mail = ""
        self.mail_server = ""
        self.attachment = ""

    # add a subject
    def add_subject(self, subject):
        self.mail_package["Subject"] = subject

    # add a destination
    def add_sender(self, sender_email=""):
        if sender_email == "":
            raise RequiredFieldEmptyError
        self.mail_package["From"] = sender_email
        self.sender_mail = sender_email

    # add add a receiving address
    def add_receiver(self, receiver_email=""):
        if receiver_email == "":
            raise RequiredFieldEmptyError
        self.mail_package["To"] = receiver_email
        self.receiver_mail = receiver_email

    # set the main required fields
    def set_required(self, sender_email, receiver_mail, subject=""):
        self.add_sender(sender_email)
        self.add_receiver(receiver_mail)
        self.add_subject(subject)

    # add a plain text message to the email
    def add_text(self, text):
        self.mail_package.attach(MIMEText(text, "plain"))

    # add a html style message to the email
    def add_html_text(self, html_text):
        self.mail_package.attach(MIMEText(html_text, "html"))

    # set the mail server
    def set_mail_server(self, mail_server="gmail"):
        """
        set the mail server address
        defaults to gmail servers

        :param mail_server:
        :return:
        """
        # todo add mail servers
        # try to add mail servers for easy mailing
        # defaults to gmail
        mail_server = mail_server.lower()
        if mail_server == "gmail":
            self.mail_server = "smtp.gmail.com"
        elif mail_server == "hotmail":
            self.mail_server = "smtp-mail.outlook.com"
        elif mail_server == "yahoo":
            self.mail_server = "smtp.mail.yahoo.com"
        else:
            self.mail_server = mail_server

    # add an attachment to the email
    def add_attachment(self, filename):
        """
        add an attachment
        use absolute path
        windows use \\ not just \

        :param filename:
        :return:
        """
        with open(filename, "rb") as attachment:
            self.attachment = MIMEBase("application", "octet-stream")
            self.attachment.set_payload(attachment.read())
        encoders.encode_base64(self.attachment)
        self.attachment.add_header("Content-Disposition",
                                   f"attachment; filename= {filename}", )
        self.mail_package.attach(self.attachment)

    # send the mail!
    def send(self, sender_mail="", password="", port=465 ,use_TLS=False):
        """
        send the email
        dont store password for safety
        your email
        :param sender_mail:
        :param port:
        optional SMTP port
        :param password:
        optional param fill with real password to not need to type
        :return:
        """
        # create a ssl context
        context = ssl.create_default_context()
        # if password is not set ask user for password
        if compare_digest(password, ""):
            password = getpass.getpass(prompt="Please enter password: ")
        if self.mail_server == "":
            self.set_mail_server()
        if not use_TLS:
            with smtplib.SMTP_SSL(self.mail_server, port, context=context) as server:
                if sender_mail == "":
                    server.login(self.sender_mail, password)
                    sender_mail = self.sender_mail
                else:
                    server.login(sender_mail, password)

                server.sendmail(sender_mail, self.receiver_mail, self.mail_package.as_string())
        elif use_TLS:
            with smtplib.SMTP(self.mail_server, port) as server:
                server.ehlo()  # Can be omitted
                server.starttls(context=context)
                server.ehlo()  # Can be omitted
                server.login(sender_mail, password)
                server.sendmail(sender_mail, self.receiver_mail, self.mail_package.as_string())
    # mail function to send many emails
    def send_many(self, addresses, sender_mail="", password="", port=465):
        context = ssl.create_default_context()
        if compare_digest(password, ""):
            password = getpass.getpass(prompt="Please enter password: ")
        if self.mail_server == "":
            self.set_mail_server()
        with smtplib.SMTP_SSL(self.mail_server, port, context=context) as server:
            if sender_mail == "":
                server.login(self.sender_mail, password)
                sender_mail = self.sender_mail
            else:
                server.login(sender_mail, password)

            for receiver in addresses:
                if len(re.findall(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",receiver)) < 1:
                    print(f"{receiver} is not a valid email address")
                else:
                    server.sendmail(sender_mail, receiver, self.mail_package.as_string())

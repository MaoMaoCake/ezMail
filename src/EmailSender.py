import smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from secrets import compare_digest


class RequiredFieldEmptyError(Exception):
    pass


class EmailSender:
    def __init__(self):
        self.mailpackgage = MIMEMultipart("alternative")

    def add_subject(self, subject):
        self.mailpackgage["Subject"] = subject

    def add_sender(self, sender_email=""):
        if sender_email == "":
            raise RequiredFieldEmptyError
        self.mailpackgage["From"] = sender_email
        self.sender_mail = sender_email

    def add_receiver(self, receiver_email=""):
        if receiver_email == "":
            raise RequiredFieldEmptyError
        self.mailpackgage["To"] = receiver_email
        self.reciever_mail = receiver_email

    def set_required(self, sender_email, receiver_mail, subject):
        self.add_sender(sender_email)
        self.add_receiver(receiver_mail)
        self.add_subject(subject)

    def add_text(self, text):
        self.mailpackgage.attach(MIMEText(text, "plain"))

    def add_html_text(self, html_text):
        self.mailpackgage.attach(MIMEText(html_text, "html"))

    def set_mail_server(self, mail_server="gmail"):
        # todo add mail servers
        mail_server = mail_server.lower()
        if mail_server == "gmail":
            self.mail_server = "smtp.gmail.com"
        elif mail_server == "hotmail":
            self.mail_server = ""
        elif mail_server == "":
            self.mail_server = ""

    def add_attachment(self, filename):
        with open(filename, "rb") as attachment:
            self.attachment = MIMEBase("application", "octet-stream")
            self.attachment.set_payload(attachment.read())
        encoders.encode_base64(self.attachment)
        self.attachment.add_header("Content-Disposition",
                                   f"attachment; filename= {filename}", )
        self.mailpackgage.attach(self.attachment)

    def send(self, sender_mail, password=""):
        context = ssl.create_default_context()
        if compare_digest(password, ""):
            password = input("Please enter password")
        with smtplib.SMTP_SSL(self.mail_server, 465, context=context) as server:
            server.login(sender_mail, password)
            server.sendmail(self.sender_mail, self.reciever_mail, self.mailpackgage.as_string())

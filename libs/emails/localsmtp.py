import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from typing import List

from libs.emails.email import Email


class LocalSMTP(Email):

    @classmethod
    def send_email(mcs, receivers: List[str], subject: str, text: str, html: str = None) -> None:
        """
        Before calling this function, start local smtp server first
        On Mac os system, type 'sudo postfix start' in terminal
        :param receivers:
        :param subject:
        :param text:
        :param html:
        :return:
        """
        message = MIMEMultipart()
        message["from"] = str(Header("Price Alert")) + mcs.SENDER
        message["to"] = ", ".join(receivers)
        message["subject"] = subject
        message.attach(MIMEText(text, 'plain'))
        message.attach(MIMEText(html, 'html'))
        try:
            server = smtplib.SMTP('localhost')
            server.set_debuglevel(1)
            server.sendmail(mcs.SENDER, receivers, message.as_string())
            server.quit()

        except smtplib.SMTPException as e:
            print("An error occurred while sending e-mail")
            print(e)


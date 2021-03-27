import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from typing import List


class EmailDelivery:
    SENDER = 'do-not-reply@price-alert.com'

    @classmethod
    def send_email_by_local_smtp(cls, receivers: List[str], subject: str, text: str, html: str = None) -> None:
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
        message["from"] = cls.SENDER
        message["to"] = ", ".join(receivers)
        message["subject"] = subject
        message.attach(MIMEText(text, 'plain'))
        message.attach(MIMEText(html, 'html'))
        try:
            server = smtplib.SMTP('localhost')
            server.set_debuglevel(1)
            server.sendmail(cls.SENDER, receivers, message.as_string())
            server.quit()

        except smtplib.SMTPException as e:
            print("An error occurred while sending e-mail")
            print(e)


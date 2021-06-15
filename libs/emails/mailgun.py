from typing import List
import requests
import os

from libs.emails.email import Email
from common.errors import EmailSendFailure

class Mailgun(Email):
    @classmethod
    def send_email(mcs, receivers: List[str], subject: str, text: str, html: str = None) -> None:
        response = requests.post(
            os.getenv("MAILGUN_URL"),
            auth=("api", os.getenv("MAILGUM_API")),
            data={
                "from": mcs.SENDER,
                "to": receivers,
                "subject": subject,
                "text": text,
                "html": html

            }
        )
        if response.status_code != 200:
            print(response.content)
        else:
            print("Email is sent successfully")






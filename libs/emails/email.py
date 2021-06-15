from abc import ABCMeta, abstractmethod
from typing import List


class Email(ABCMeta):
    SENDER = 'do-not-reply@price-alert.com'

    @abstractmethod
    def send_email(cls, receivers: List[str], subject: str, text: str, html: str = None):
        pass
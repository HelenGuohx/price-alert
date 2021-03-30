from typing import Dict, List
import requests
from bs4 import BeautifulSoup
import re
import uuid
from dataclasses import dataclass, field

from models.model import Model
from common.errors import HTMLElementNotMatched, RequestFailureError


@dataclass(eq=False)
class Item(Model):
    collection: str = field(init=False, default="items")
    url: str
    tag_name: str
    query: Dict
    price: float = field(default=None)
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:86.0) Gecko/20100101 Firefox/86.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Sec-WebSocket-Version": "13",
    "Sec-WebSocket-Extensions": "permessage-deflate",
    "Sec-WebSocket-Key": "MW7/zV09JfaRpM+jEHrdBA==",
    "Connection": "keep-alive, Upgrade",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "Upgrade": "websocket",
    }

    def load_price(self) -> float:
        # add header to request???
        response = requests.get(self.url, headers=self.headers)
        if response.status_code != 200:
            raise RequestFailureError("Request failure")

        soup = BeautifulSoup(response.content, "html.parser")
        element = soup.find(self.tag_name, self.query)
        if element is None:
            raise HTMLElementNotMatched(f"Can't find element in {self.url} with tag_name={self.tag_name} and query={self.query}")

        string_price = element.text.strip()

        pattern = re.compile(r"\d+,?\d*\.?\d+")
        match = pattern.search(string_price)
        found_group = match.group(0)
        price = found_group.replace(",", "")
        self.price = float(price)
        return self.price

    def json(self) -> Dict:
        return {
            "_id": self._id,
            "url": self.url,
            "tag_name": self.tag_name,
            "query": self.query,
            "price": self.price,
        }



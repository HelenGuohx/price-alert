from typing import Dict, List
import requests
from bs4 import BeautifulSoup
import re
import uuid
from dataclasses import dataclass, field

from models.model import Model


@dataclass(eq=False)
class Item(Model):
    collection: str = field(init=False, default="items")
    url: str
    tag_name: str
    query: Dict
    price: float = field(default=None)
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    def load_price(self) -> float:
        # add header to request???
        response = requests.get(self.url, verify=False)
        if response.status_code != 200:
            raise Exception("Request failure")

        soup = BeautifulSoup(response.content, "html.parser")
        element = soup.find(self.tag_name, self.query)
        if element is None:
            raise Exception(f"Can't find element in {self.url} with tag_name={self.tag_name} and query={self.query}")

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



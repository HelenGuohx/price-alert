from dataclasses import dataclass, field
import uuid
import re
from typing import Dict
from models.model import Model

@dataclass(eq=False)
class Store(Model):
    collection: str = field(init=False, default="stores")
    name: str
    url_prefix: str
    tag_name: str
    query: Dict
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    def json(self) -> Dict:
        return {
            "_id": self._id,
            "name": self.name,
            "url_prefix": self.url_prefix,
            "tag_name": self.tag_name,
            "query": self.query
        }

    @classmethod
    def get_by_name(cls, store_name) -> "Store":
        return cls.find_one_by("name", store_name)


    @classmethod
    def get_by_url_prefix(cls, url_prefix) -> "Store":
        pattern = "^{}".format(url_prefix)
        url_regex = {"$regex": pattern}
        return cls.find_one_by("url_prefix", url_regex)

    @classmethod
    def find_by_url(cls, url) -> "Store":
        """
        Return a store from a url
        :param url: The item's url
        :return: a store
        """
        pattern = re.compile("(https?://.*?)/")
        url_prefix = pattern.search(url).group(1)

        return cls.get_by_url_prefix(url_prefix)
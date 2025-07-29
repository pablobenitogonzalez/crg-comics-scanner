import hashlib
from enum import Enum

from bs4 import BeautifulSoup

import _request
import _web

SELECTORS = [
    'a[href*=ed2k]',
    'area[href*=ed2k]'
]


# noinspection HttpUrlsUsage
class Protocol(Enum):
    HTTP = 'http://'
    ED2K = 'ed2k://'


class Property(Enum):
    TOPIC_ID = 'topic_id'
    TOPIC_LINK = 'topic_link'
    ED2KS = 'ed2ks'
    AUDIT_HASH = 'audit_hash'


class Topic:

    def __init__(self, rq_manager: _request.RequestManager, topic_id: int):
        self._topic_id: int = topic_id
        self._topic_link: str = _web.topic_url.format(_web.protocol, self._topic_id)
        html_topic = rq_manager.get_html(self._topic_link)
        soup_topic = BeautifulSoup(html_topic, 'html.parser')
        ed2k_links = []
        for selector in SELECTORS:
            ed2k_links += soup_topic.select(selector)
        self._ed2ks: list = self.__extract_ed2ks(ed2k_links)
        self._audit_hash: str = hashlib.sha1(';'.join([self._topic_id, self._topic_link]).encode()).hexdigest()

    # noinspection HttpUrlsUsage
    @staticmethod
    def __extract_ed2ks(ed2k_links) -> list:
        clean_ed2ks = []
        if not ed2k_links:
            return clean_ed2ks
        for ed2k_link in ed2k_links:
            href = ed2k_link['href']
            if href.startswith(Protocol.HTTP.value):
                href = href.replace(Protocol.HTTP.value, '')
            if href.startswith(Protocol.ED2K.value):
                e = href.split('%7C') if '%7C' in href else href.split('|')
                if len(e) >= 5:
                    clean_ed2ks.append(href)
        return clean_ed2ks

    @property
    def topic_id(self) -> int:
        return self._topic_id

    @property
    def topic_link(self) -> str:
        return self._topic_link

    @property
    def ed2ks(self) -> list:
        return self._ed2ks

    @property
    def audit_hash(self) -> str:
        return self._audit_hash

    @topic_id.setter
    def topic_id(self, topic_id: int):
        self._topic_id = topic_id

    @topic_link.setter
    def topic_link(self, topic_link: str):
        self._topic_link = topic_link

    @ed2ks.setter
    def ed2ks(self, ed2ks: list):
        self._ed2ks = ed2ks

    @audit_hash.setter
    def audit_hash(self, audit_hash: str):
        self._audit_hash = audit_hash

    def to_dict(self):
        return {
            Property.TOPIC_ID.value: self._topic_id,
            Property.TOPIC_LINK.value: self._topic_link,
            Property.ED2KS.value: self._ed2ks,
            Property.AUDIT_HASH.value: self._audit_hash
        }

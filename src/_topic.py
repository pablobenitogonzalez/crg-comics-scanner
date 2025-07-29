import hashlib
from datetime import datetime
from enum import Enum

import pytz as pytz
from bs4 import BeautifulSoup

import _forum
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
    TOPIC_OWNER = 'topic_owner'
    TOPIC_CREATED = 'topic_created'
    TOPIC_TITLE = 'topic_title'
    TOPIC_DESCRIPTION = 'topic_description'
    CRG_LIBRARY = 'crg_library'
    CRG_GROUP = 'crg_group'
    CRG_KEY = 'crg_key'
    ED2KS = 'ed2ks'
    AUDIT_HASH = 'audit_hash'


class Topic:
    def __init__(self, rq_manager: _request.RequestManager, forum: _forum.Forum, tds: list):
        self._topic_id: int = tds[2].find('span')['id'].replace('tid-span-', '')
        self._topic_link: str = _web.topic_url.format(_web.protocol, self._topic_id)
        owner_link = tds[4].find('a')
        self._topic_owner: str = owner_link.text if owner_link else tds[4].text
        self._topic_created = None
        self._topic_created_str: str = ''
        self._topic_title: str = tds[2].find('a', {'id': f'tid-link-{self._topic_id}'}).text
        self._topic_description: str = tds[2].find('span', {'id': f'tid-desc-{self._topic_id}'}).text
        try:
            created_str = tds[4].find('span').text
            self._topic_created: datetime = datetime.strptime(created_str, '%b %d %Y, %H:%M') \
                .astimezone(pytz.timezone('Europe/Madrid'))
            self._topic_created_str = self._topic_created.isoformat()
        except Exception as e:
            print(f'[ERROR] Cannot parse topic created datetime: {e}')
        self._crg_library: str = forum.library
        self._crg_group: str = forum.group
        self._crg_key: str = forum.key

        html_topic = rq_manager.get_html(self._topic_link)
        soup_topic = BeautifulSoup(html_topic, 'html.parser')
        ed2k_links = []
        for selector in SELECTORS:
            ed2k_links += soup_topic.select(selector)
        self._ed2ks: list = self.__extract_ed2ks(ed2k_links)

        self._audit_hash: str = hashlib.sha1(';'.join([self._topic_id,
                                                       self._topic_link,
                                                       self._topic_owner,
                                                       self._topic_created_str,
                                                       self._topic_title,
                                                       self._topic_description,
                                                       self._crg_library,
                                                       self._crg_group,
                                                       self._crg_key]).encode()).hexdigest()

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
    def topic_owner(self) -> str:
        return self._topic_owner

    @property
    def topic_created(self) -> datetime:
        return self._topic_created

    @property
    def topic_created_str(self) -> str:
        return self._topic_created_str

    @property
    def topic_title(self) -> str:
        return self._topic_title

    @property
    def topic_description(self) -> str:
        return self._topic_description

    @property
    def crg_library(self) -> str:
        return self._crg_library

    @property
    def crg_group(self) -> str:
        return self._crg_group

    @property
    def crg_key(self) -> str:
        return self._crg_key

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

    @topic_owner.setter
    def topic_owner(self, topic_owner: str):
        self._topic_owner = topic_owner

    @topic_created.setter
    def topic_created(self, topic_created: datetime):
        self._topic_created = topic_created

    @topic_created_str.setter
    def topic_created_str(self, topic_created_str: str):
        self._topic_created_str = topic_created_str

    @topic_title.setter
    def topic_title(self, topic_title: str):
        self._topic_title = topic_title

    @topic_description.setter
    def topic_description(self, topic_description: str):
        self._topic_description = topic_description

    @crg_library.setter
    def crg_library(self, crg_library: _forum.Library):
        self._crg_library = crg_library

    @crg_group.setter
    def crg_group(self, crg_group: _forum.Group):
        self._crg_group = crg_group

    @crg_key.setter
    def crg_key(self, crg_key: _forum.Key):
        self._crg_key = crg_key

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
            Property.TOPIC_OWNER.value: self._topic_owner,
            Property.TOPIC_CREATED.value: self._topic_created_str,
            Property.TOPIC_TITLE.value: self._topic_title,
            Property.TOPIC_DESCRIPTION.value: self._topic_description,
            Property.CRG_LIBRARY.value: self._crg_library,
            Property.CRG_GROUP.value: self._crg_group,
            Property.CRG_KEY.value: self._crg_key,
            Property.ED2KS.value: self._ed2ks,
            Property.AUDIT_HASH.value: self._audit_hash
        }

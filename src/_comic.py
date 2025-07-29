import urllib.parse
from datetime import datetime
from enum import Enum

import _topic


# noinspection HttpUrlsUsage
class Protocol(Enum):
    HTTP = 'http://'
    ED2K = 'ed2k://'


class Property(Enum):
    ED2K_MD4 = 'ed2k_md4'
    ED2K_FILE_NAME = 'ed2k_file_name'
    ED2K_LINK = 'ed2k_link'
    TOPIC_ID = 'topic_id'
    TOPIC_LINK = 'topic_link'
    TOPIC_OWNER = 'topic_owner'
    TOPIC_CREATED = 'topic_created'
    TOPIC_TITLE = 'topic_title'
    TOPIC_DESCRIPTION = 'topic_description'
    CRG_LIBRARY = 'crg_library'
    CRG_GROUP = 'crg_group'
    CRG_KEY = 'crg_key'
    AUDIT_HASH = 'audit_hash'


class Comic:
    def __init__(self, topic: _topic.Topic, ed2k: str):
        e = ed2k.split('%7C') if '%7C' in ed2k else ed2k.split('|')
        self._ed2k_md4: str = e[4]
        self._ed2k_file_name: str = urllib.parse.unquote(e[2])
        self._ed2k_link: str = ed2k
        self._topic: _topic.Topic = topic

    @property
    def ed2k_md4(self) -> str:
        return self._ed2k_md4

    @property
    def ed2k_file_name(self) -> str:
        return self._ed2k_file_name

    @property
    def ed2k_link(self) -> str:
        return self._ed2k_link

    @property
    def topic_id(self) -> int:
        return self._topic.topic_id

    @property
    def topic_link(self) -> str:
        return self._topic.topic_link

    @property
    def topic_owner(self) -> str:
        return self._topic.topic_owner

    @property
    def topic_created(self) -> datetime:
        return self._topic.topic_created

    @property
    def topic_created_str(self) -> str:
        return self._topic.topic_created_str

    @property
    def topic_title(self) -> str:
        return self._topic.topic_title

    @property
    def topic_description(self) -> str:
        return self._topic.topic_description

    @property
    def crg_library(self) -> str:
        return self._topic.crg_library

    @property
    def crg_group(self) -> str:
        return self._topic.crg_group

    @property
    def crg_key(self) -> str:
        return self._topic.crg_key

    @property
    def audit_hash(self) -> str:
        return self._topic.audit_hash

    def to_dict(self):
        return {
            Property.ED2K_MD4.value: self._ed2k_md4,
            Property.ED2K_FILE_NAME.value: self._ed2k_file_name,
            Property.ED2K_LINK.value: self._ed2k_link,
            Property.TOPIC_ID.value: self.topic_id,
            Property.TOPIC_LINK.value: self.topic_link,
            Property.TOPIC_OWNER.value: self.topic_owner,
            Property.TOPIC_CREATED.value: self.topic_created_str,
            Property.TOPIC_TITLE.value: self.topic_title,
            Property.TOPIC_DESCRIPTION.value: self.topic_description,
            Property.CRG_LIBRARY.value: self.crg_library,
            Property.CRG_GROUP.value: self.crg_group,
            Property.CRG_KEY.value: self.crg_key,
            Property.AUDIT_HASH.value: self.audit_hash
        }

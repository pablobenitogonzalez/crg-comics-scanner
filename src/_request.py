import os
import random
import time
from enum import Enum

import requests
from retry import retry

import _logging
import _web


class EnvProperty(Enum):
    CRG_USER = 'CRG_USER'
    CRG_PASS = 'CRG_PASS'

CRG_USER = os.getenv(EnvProperty.CRG_USER.value, "unknown")
CRG_PASS = os.getenv(EnvProperty.CRG_PASS.value, "unknown")


# noinspection HttpUrlsUsage
class LoginDataProperty(Enum):
    REFERER = 'referer'
    USER = 'UserName'
    PASSWORD = 'PassWord'
    COOKIE_DATE = 'CookieDate'


class HeaderProperty(Enum):
    ACCEPT = 'Accept'
    ACCEPT_ENCODING = 'Accept-Encoding'
    ACCEPT_LANGUAGE = 'Accept-Language'
    CACHE_CONTROL = 'Cache-Control'
    CONNECTION = 'Connection'
    HOST = 'Host'
    PRAGMA = 'Pragma'
    UPGRADE_INSECURE_REQUESTS = 'Upgrade-Insecure-Requests'
    USER_AGENT = 'User-Agent'


class RequestManager:
    def __init__(self):
        self._min_delay = 0.5
        self._max_delay = 1.0
        self._timeout = 5

    @retry(Exception, delay=3, tries=3, backoff=2)
    def get_html(self, url):
        try:
            sleep_duration = random.uniform( self._min_delay, self._max_delay)
            _logging.debug(f"-----Waiting {sleep_duration:.2f} seconds before next request-----")
            time.sleep(sleep_duration)  # rate limit issues
            session = requests.Session()
            login_url = _web.login_url.format(_web.protocol)
            form_data = {
                LoginDataProperty.REFERER.value: login_url,
                LoginDataProperty.USER.value: CRG_USER,
                LoginDataProperty.PASSWORD.value: CRG_PASS,
                LoginDataProperty.COOKIE_DATE.value: '1'
            }
            session.post(login_url, data=form_data)
            headers = {
                HeaderProperty.ACCEPT.value: 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,'
                                             'image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                HeaderProperty.ACCEPT_ENCODING.value: 'gzip, deflate',
                HeaderProperty.ACCEPT_LANGUAGE.value: 'es-ES,es;q=0.9,en;q=0.8',
                HeaderProperty.CACHE_CONTROL.value: 'no-cache',
                HeaderProperty.CONNECTION.value: 'keep-alive',
                HeaderProperty.HOST.value: 'lamansion-crg.net',
                HeaderProperty.PRAGMA.value: 'no-cache',
                HeaderProperty.UPGRADE_INSECURE_REQUESTS.value: '1',
                HeaderProperty.USER_AGENT.value: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                                 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'
            }
            response = session.get(url, headers=headers, timeout=self._timeout)
            if response.status_code != 200:
                raise Exception(f'Server responded with status code {response.status_code}')
            return response.text
        except Exception as e:
            _logging.error(f'[ERROR] {e}')
            raise e

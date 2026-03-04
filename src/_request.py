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


class LoginDataProperty(Enum):
    REFERER = 'referer'
    USER = 'UserName'
    PASSWORD = 'PassWord'
    COOKIE_DATE = 'CookieDate'


class HeaderProperty(Enum):
    ACCEPT = 'Accept'
    ACCEPT_LANGUAGE = 'Accept-Language'
    REFERER = 'Referer'
    ORIGIN = 'Origin'
    USER_AGENT = 'User-Agent'


# noinspection HttpUrlsUsage
class RequestManager:
    def __init__(self):
        self._min_delay = 0.5
        self._max_delay = 1.0
        self._session = requests.Session()
        self._authenticate()

    def _authenticate(self):
        _logging.info("Authenticating...")
        login_url = _web.login_url.format(_web.protocol)
        common_headers = {
            HeaderProperty.USER_AGENT.value: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                                             '(KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
            HeaderProperty.ACCEPT_LANGUAGE.value: 'es-ES,es;q=0.9,en;q=0.8',
        }
        self._session.get(login_url, headers=common_headers, timeout=10)
        headers_login = {
            **common_headers,
            HeaderProperty.REFERER.value: login_url,
            HeaderProperty.ORIGIN.value: 'http://lamansion-crg.net'
        }
        form_data = {
            LoginDataProperty.REFERER.value: login_url,
            LoginDataProperty.USER.value: CRG_USER,
            LoginDataProperty.PASSWORD.value: CRG_PASS,
            LoginDataProperty.COOKIE_DATE.value: '1'
        }
        response = self._session.post(login_url, data=form_data, headers=headers_login, timeout=15)
        if 'Contraseña' in response.text:
            error_msg = 'Login error, invalid credentials.'
            _logging.error(error_msg)
            raise Exception(error_msg)

        _logging.info("Authentication completed.")

    def clear_read_cookies(self):
        """ Removes the 'foro_nuevotopicsread' cookie from the session.
        This prevents the 'HTTP 400 Bad Request' error caused by
        excessive header size when the forum tracks too many read topics.
        """
        self._session.cookies.pop('foro_nuevotopicsread', None)
        _logging.debug("Read-topics cookie cleared to prevent header overflow.")

    @retry(Exception, delay=3, tries=3, backoff=2)
    def get_html(self, url):
        try:
            sleep_duration = random.uniform(self._min_delay, self._max_delay)
            _logging.debug(f"-----Waiting {sleep_duration:.2f} seconds before next request-----")
            time.sleep(sleep_duration)

            headers_get = {
                HeaderProperty.ACCEPT.value: 'text/html,application/xhtml+xml,application/xml;q=0.9,'
                                             'image/avif,image/webp,*/*;q=0.8',
                HeaderProperty.USER_AGENT.value: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                                                 '(KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'
            }
            response = self._session.get(url, headers=headers_get, timeout=15)

            if 'act=Login' in response.url:
                self._authenticate()
                raise Exception('Session expired')

            return response.text

        except Exception as e:
            _logging.error(f'[ERROR] {e}')
            raise e

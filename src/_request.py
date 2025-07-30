import random
import time
from enum import Enum

import requests
from retry import retry

import _logging
import _web


# noinspection HttpUrlsUsage
class LoginDataProperty(Enum):
    REFERER = 'referer'
    USER = 'UserName'
    PASSWORD = 'PassWord'
    COOKIE_DATE = 'CookieDate'


class RequestManager:
    def __init__(self):
        self._min_delay = 1.0
        self._max_delay = 2.0
        self._timeout = 5
        self._session = requests.Session()
        login_url = _web.login_url.format(_web.protocol)
        form_data = {
            LoginDataProperty.REFERER.value: login_url,
            LoginDataProperty.USER.value: 'zedreno',
            LoginDataProperty.PASSWORD.value: 'p12b02g78',
            LoginDataProperty.COOKIE_DATE.value: '1'
        }
        try:
            self._session.post(login_url, data=form_data)
        except Exception as e:
            _logging.error(f'[ERROR] {e}')
            raise e

    @retry(Exception, delay=5, tries=5, backoff=5)
    def get_html(self, url):
        try:
            sleep_duration = random.uniform( self._min_delay, self._max_delay)
            _logging.debug(f"-----Waiting {sleep_duration:.2f} seconds before next request-----")
            time.sleep(sleep_duration)  # rate limit issues
            response = self._session.get(url, timeout=self._timeout)
            if response.status_code != 200:
                raise Exception(f'Server responded with status code {response.status_code}')
            return response.text
        except Exception as e:
            _logging.error(f'[ERROR] {e}')
            raise e

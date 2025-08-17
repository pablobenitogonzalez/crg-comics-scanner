import os
from enum import Enum

import psycopg2

import _comic
import _scan


class EnvProperty(Enum):
    DB_HOST = 'DB_HOST'
    DB_PORT = 'DB_PORT'
    DB_NAME = 'DB_NAME'
    DB_USER = 'DB_USER'
    DB_PASS = 'DB_PASS'

DB_HOST = os.getenv(EnvProperty.DB_HOST.value, "192.168.50.69")
DB_PORT = os.getenv(EnvProperty.DB_PORT.value, "5436")
DB_NAME = os.getenv(EnvProperty.DB_NAME.value, "crg")
DB_USER = os.getenv(EnvProperty.DB_USER.value, "crg")
DB_PASS = os.getenv(EnvProperty.DB_PASS.value, "crg")


class DatabaseManager:
    def __init__(self):
        self._conn = psycopg2.connect(user=DB_USER,
                                      password=DB_PASS,
                                      host=DB_HOST,
                                      port=DB_PORT,
                                      database=DB_NAME)

    def close_conn(self):
        self._conn.close()

    def __execute(self, sql, values):
        cursor = self._conn.cursor()
        with self._conn:
            with cursor as cur:
                cur.execute(sql, values)
        self._conn.commit()

    def find_db_comic_hash(self, ed2k_md4: str):
        query = '''
                select audit_hash from comics where ed2k_md4 = %s \
                '''
        cursor = self._conn.cursor()
        with self._conn:
            with cursor as cur:
                cur.execute(query, [ed2k_md4])
                result = cur.fetchone()
                return result[0] if result and len(result) > 0 else None

    def create_comic(self, comic: _comic.Comic):
        sql = '''
              insert into comics (ed2k_md4, ed2k_file_name, ed2k_link, topic_id, topic_link, audit_created,
                                  audit_updated, audit_hash) values (%s, %s, %s, %s, %s, (now() at time zone 'utc'::text),
                                                                     (now() at time zone 'utc'::text), %s) \
              '''
        values = (comic.ed2k_md4, comic.ed2k_file_name, comic.ed2k_link, comic.topic_id, comic.topic_link,
                  comic.audit_hash)
        self.__execute(sql, values)

    def save_scan(self, scan: _scan.Scan):
        sql = '''
              insert into comics_scans ("result", started, finished, elapsed, total_topics, topics_processed, scanned,
                                        added, exception_type, exception_message, exception_stacktrace, audit_created)
              values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, (now() at time zone 'utc'::text)) \
              '''
        values = (scan.result, scan.started, scan.finished, scan.elapsed, scan.total_topics, scan.topics_processed,
                  scan.scanned, scan.added, scan.exception_type, scan.exception_message, scan.exception_stacktrace)
        self.__execute(sql, values)


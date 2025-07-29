import json

import psycopg2

import _comic
import _scan


class DatabaseManager:
    def __init__(self):
        self._conn = psycopg2.connect(user="crg",
                                      password="crg",
                                      host="192.168.50.74",
                                      port="5433",
                                      database="crg")

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
            select audit_hash from comics where ed2k_md4 = %s
        '''
        cursor = self._conn.cursor()
        with self._conn:
            with cursor as cur:
                cur.execute(query, [ed2k_md4])
                result = cur.fetchone()
                return result[0] if result and len(result) > 0 else None

    def create_comic(self, comic: _comic.Comic):
        sql = '''
            insert into comics (ed2k_md4, ed2k_file_name, ed2k_link, topic_id, topic_link, topic_owner, topic_created, 
            topic_created_str, topic_title, topic_description, crg_library, crg_group, crg_key, audit_created,
             audit_updated, audit_hash) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
             (now() at time zone 'utc'::text), (now() at time zone 'utc'::text), %s)
        '''
        values = (comic.ed2k_md4, comic.ed2k_file_name, comic.ed2k_link, comic.topic_id, comic.topic_link,
                  comic.topic_owner, comic.topic_created, comic.topic_created_str, comic.topic_title,
                  comic.topic_description, comic.crg_library, comic.crg_group, comic.crg_key, comic.audit_hash)
        self.__execute(sql, values)

    def update_comic(self, comic: _comic.Comic):
        sql = '''
            update comics set ed2k_file_name = %s, ed2k_link = %s, topic_id = %s, topic_link = %s, topic_owner = %s, 
            topic_created = %s, topic_created_str = %s, topic_title = %s, topic_description = %s, crg_library = %s, 
            crg_group = %s,  crg_key = %s, audit_updated = (now() at time zone 'utc'::text), audit_hash = %s 
            where ed2k_md4 = %s
        '''
        values = (comic.ed2k_file_name, comic.ed2k_link, comic.topic_id, comic.topic_link, comic.topic_owner,
                  comic.topic_created, comic.topic_created_str, comic.topic_title, comic.topic_description,
                  comic.crg_library, comic.crg_group, comic.crg_key, comic.audit_hash, comic.ed2k_md4)
        self.__execute(sql, values)

    def save_scan(self, scan: _scan.Scan):
        sql = '''
            insert into scans ("type", "result", started, finished, elapsed, scanned, skipped, added, updated, details, 
            exception_type, exception_message, exception_stacktrace, audit_created) values (%s, %s, %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s, %s, (now() at time zone 'utc'::text))
        '''
        values = (scan.type, scan.result, scan.started, scan.finished, scan.elapsed, scan.scanned, scan.skipped,
                  scan.added, scan.updated, json.dumps(scan.details, default=str), scan.exception_type,
                  scan.exception_message, scan.exception_stacktrace)
        self.__execute(sql, values)


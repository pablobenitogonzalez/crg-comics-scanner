import json
import os
import time
import traceback
from enum import Enum

import _comic
import _database
import _file
import _logging
import _request
import _scan
import _topic


class EnvProperty(Enum):
    DELAY = 'delay'
    MAX_TOPICS = 'max_topics'

DELAY = int(os.getenv(EnvProperty.DELAY.value, 600))  # default 10 minutes
MAX_TOPICS = int(os.getenv(EnvProperty.MAX_TOPICS.value, 50)) # default 50

scan = _scan.Scan()
rq_manager = _request.RequestManager()
db_manager = _database.DatabaseManager()
file_manager = _file.FileManager()
try:

    topic_ids = file_manager.read()
    scan.total_topics = len(topic_ids)
    idx_topic = 0
    idx_scanned = 0
    idx_added = 0

    for topic_id in topic_ids:

        idx_topic += 1
        if (idx_topic % MAX_TOPICS) == 0:
            _logging.debug(f'-----Waiting {DELAY} second/s for rate limit (next topic to process is {idx_topic})-----')
            time.sleep(DELAY)

        topic = _topic.Topic(rq_manager, topic_id[0])
        _logging.info(f'[TOPIC {idx_topic}] {topic.topic_link}')
        for ed2k in topic.ed2ks:

            comic = _comic.Comic(topic, ed2k)
            db_hash = db_manager.find_db_comic_hash(comic.ed2k_md4)

            if not db_hash:
                db_manager.create_comic(comic)
                idx_scanned += 1
                idx_added += 1
                _logging.info(f'>>> added <<< {comic.to_dict()}')
                continue

            idx_scanned += 1

    # manage totals
    scan.scanned = scan.scanned + idx_scanned
    scan.added =  scan.added + idx_added
    scan.topics_processed = idx_topic

except Exception as e:
    _logging.error(f'[ERROR] {e}')
    scan.exception_type = e.__class__.__name__
    scan.exception_message = getattr(e, 'message', str(e))
    scan.exception_stacktrace = traceback.format_exc()

scan.finish_scan(_scan.Result.SUCCESS if not scan.exception_type else _scan.Result.ERROR)
_logging.info(json.dumps(
    scan.to_dict(),
    indent=4,
    separators=(',', ': ')
))
db_manager.save_scan(scan)
db_manager.close_conn()

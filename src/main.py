import json
import traceback
from enum import Enum

from bs4 import BeautifulSoup

import _comic
import _database
import _forum
import _logger
import _request
import _scan
import _web
import _topic

ST_INCREMENT = 30


class DetailOutput(Enum):
    SCANNED = 'scanned'
    SKIPPED = 'skipped'
    ADDED = 'added'
    UPDATED = 'updated'
    NOT_PROCESSED = 'not_processed'


scan = _scan.Scan(_scan.Type.COMICS)
rq_manager = _request.RequestManager()
db_manager = _database.DatabaseManager()
try:

    forums = _forum.Forum.list()
    for forum_str in forums:

        idx_scanned = 0
        idx_skipped = 0
        idx_added = 0
        idx_updated = 0
        not_processed = []
        pos = -30
        forum = _forum.Forum(forum_str)
        while True:

            pos += ST_INCREMENT
            url = f'{_web.forum_url.format(_web.protocol, forum.code)}{_web.page_args.format(pos)}'

            try:
                html = rq_manager.get_html(url)
                soup = BeautifulSoup(html, 'html.parser')
                tables = soup.find_all('table', {'class': 'ipbtable', 'cellspacing': '1'})
                topics_table = tables[len(tables)-1]
                trs = topics_table.select('tr')

                if len(trs) <= 4:  # control pagination
                    break

                for tr in trs:

                    try:
                        th = tr.select('th')
                        if len(th) != 0:
                            continue
                        tds = tr.find_all('td')
                        if len(tds) < 6:
                            continue
                        td_pinned = tds[1].select('img[alt*=Pinned]')
                        if len(td_pinned) > 0:
                            continue

                        topic = _topic.Topic(rq_manager, forum, tds)
                        for ed2k in topic.ed2ks:

                            comic = _comic.Comic(topic, ed2k)
                            db_hash = db_manager.find_db_comic_hash(comic.ed2k_md4)

                            if not db_hash:
                                db_manager.create_comic(comic)
                                idx_scanned += 1
                                idx_added += 1
                                _logger.info(f'{idx_scanned}: >>> added <<< {comic.to_dict()}')
                                continue

                            if db_hash != comic.audit_hash:
                                db_manager.update_comic(comic)
                                idx_scanned += 1
                                idx_updated += 1
                                _logger.info(f'{idx_scanned}: >>> updated <<< {comic.to_dict()}')
                                continue

                            idx_scanned += 1
                            idx_skipped += 1
                            _logger.info(f'{idx_scanned}: >>> skipped <<< {comic.to_dict()}')

                    except Exception as e:
                      error_msg = f'[ERROR] {url} - {e} - {traceback.format_exc()}'
                      not_processed.append(str(tr))

            except Exception as e:
                error_msg = f'[ERROR] {url} - {e} - {traceback.format_exc()}'
                print(error_msg)
                raise Exception(error_msg)

        # manage totals
        scan.inc_scanned(idx_scanned)
        scan.inc_skipped(idx_skipped)
        scan.inc_added(idx_added)
        scan.inc_updated(idx_updated)

        # manage details
        if forum.library not in scan.details:
            scan.details[forum.library] = {}
        if forum.group not in scan.details[forum.library]:
            scan.details[forum.library][forum.group] = {}
        if forum.key not in scan.details[forum.library][forum.group]:
            scan.details[forum.library][forum.group][forum.key] = {}
        scan.details[forum.library][forum.group][forum.key][DetailOutput.SCANNED.value] = idx_scanned
        scan.details[forum.library][forum.group][forum.key][DetailOutput.SKIPPED.value] = idx_skipped
        scan.details[forum.library][forum.group][forum.key][DetailOutput.ADDED.value] = idx_added
        scan.details[forum.library][forum.group][forum.key][DetailOutput.UPDATED.value] = idx_updated
        print(f'>>>>>> {len(not_processed)} tr/s not processed')
        scan.details[forum.library][forum.group][forum.key][DetailOutput.NOT_PROCESSED.value] = not_processed
        for tr in not_processed:
            print(f'>>>>>> {tr}')

except Exception as e:
    print(f'[ERROR] {e}')
    scan.exception_type = e.__class__.__name__
    scan.exception_message = getattr(e, 'message', str(e))
    scan.exception_stacktrace = traceback.format_exc()

scan.finish_scan(_scan.Result.SUCCESS if not scan.exception_type else _scan.Result.ERROR)
print(json.dumps(
    scan.to_dict(),
    indent=4,
    separators=(',', ': ')
))
db_manager.save_scan(scan)
db_manager.close_conn()

import datetime
import os
import re

READING_PATH = '../reading'
ED2K_LINKS_PATH = '../ed2klinks'
ED2K_LINKS_SIZE = 50


class FileManager:
    @staticmethod
    def read() -> list:
        topics = []
        folders = os.listdir(READING_PATH)
        for folder in folders:
            topic = re.findall(r'\[([^]]*)\]', folder)
            if len(topic) > 0:
                topics.append(topic)
        return topics

    @staticmethod
    def write(topic: int, ed2ks: list) -> int:
        file_datetime = datetime.datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        groups = [ed2ks[i:i + ED2K_LINKS_SIZE] for i in range(0, len(ed2ks), ED2K_LINKS_SIZE)]
        for gid, group in enumerate(groups):
            ed2k_links_file = f'{ED2K_LINKS_PATH}/[{topic}]_{file_datetime}_{str(gid).zfill(3)}.txt'
            with open(ed2k_links_file, 'w', encoding='utf-8') as f:
                for eid, ed2k in enumerate(group):
                    f.write(f'{ed2k[0]}\n')
        return len(groups)

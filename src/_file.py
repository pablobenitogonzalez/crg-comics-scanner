import os
import re

READING_PATH = '../reading'

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

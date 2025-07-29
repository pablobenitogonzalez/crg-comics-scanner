from datetime import datetime, UTC
from enum import Enum


class Property(Enum):
    TYPE = 'type'
    RESULT = 'result'
    STARTED = 'started'
    FINISHED = 'finished'
    ELAPSED = 'elapsed'
    TOTAL_TOPICS = 'total_topics'
    SCANNED = 'scanned'
    ADDED = 'added'
    EXCEPTION_TYPE = 'exception_type'
    EXCEPTION_MESSAGE = 'exception_message'
    EXCEPTION_STACKTRACE = 'exception_stacktrace'


class Result(Enum):
    PROCESSING = 'processing'
    SUCCESS = 'success'
    ERROR = 'error'


class Scan:
    def __init__(self):
        self._result: Result = Result.PROCESSING
        self._started: datetime = datetime.now(UTC)
        self._finished = None
        self._elapsed: str = ''
        self._total_topics: int = 0
        self._scanned: int = 0
        self._added: int = 0
        self._exception_type = None
        self._exception_message = None
        self._exception_stacktrace = None

    @property
    def result(self) -> str:
        return self._result.value

    @property
    def started(self) -> datetime:
        return self._started

    @property
    def started_str(self) -> str:
        return self._started.isoformat()

    @property
    def finished(self) -> datetime:
        return self._finished

    @property
    def finished_str(self) -> str:
        return self._finished.isoformat() if self._finished else ''

    @property
    def elapsed(self) -> str:
        return self._elapsed

    @property
    def total_topics(self) -> int:
        return self._total_topics

    @property
    def scanned(self) -> int:
        return self._scanned

    @property
    def added(self) -> int:
        return self._added

    @property
    def exception_type(self) -> str:
        return self._exception_type

    @property
    def exception_message(self) -> str:
        return self._exception_message

    @property
    def exception_stacktrace(self) -> str:
        return self._exception_stacktrace

    def finish_scan(self, result: Result):
        self._result = result
        self._finished: datetime = datetime.now(UTC)
        self._elapsed = str(self._finished - self._started)

    @total_topics.setter
    def total_topics(self, total_topics: int):
        self._total_topics = total_topics

    @scanned.setter
    def scanned(self, scanned: int):
        self._scanned = scanned

    @added.setter
    def added(self, added: int):
        self._added = added

    @exception_type.setter
    def exception_type(self, exception_type: str):
        self._exception_type = exception_type

    @exception_message.setter
    def exception_message(self, exception_message: str):
        self._exception_message = exception_message

    @exception_stacktrace.setter
    def exception_stacktrace(self, exception_stacktrace: str):
        self._exception_stacktrace = exception_stacktrace

    def to_dict(self):
        json = {
            Property.RESULT.value: self._result.value,
            Property.STARTED.value: self.started_str,
            Property.FINISHED.value: self.finished_str,
            Property.ELAPSED.value: self._elapsed,
            Property.TOTAL_TOPICS.value: self._total_topics,
            Property.SCANNED.value: self._scanned,
            Property.ADDED.value: self._added
        }
        if self._exception_type:
            json[Property.EXCEPTION_TYPE.value] = self._exception_type
        if self._exception_message:
            json[Property.EXCEPTION_MESSAGE.value] = self._exception_message
        if self._exception_stacktrace:
            json[Property.EXCEPTION_STACKTRACE.value] = self._exception_stacktrace
        return json

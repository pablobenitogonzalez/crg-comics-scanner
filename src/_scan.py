from datetime import datetime
from enum import Enum


class Property(Enum):
    TYPE = 'type'
    RESULT = 'result'
    STARTED = 'started'
    FINISHED = 'finished'
    ELAPSED = 'elapsed'
    SCANNED = 'scanned'
    SKIPPED = 'skipped'
    ADDED = 'added'
    UPDATED = 'updated'
    DETAILS = 'details'
    EXCEPTION_TYPE = 'exception_type'
    EXCEPTION_MESSAGE = 'exception_message'
    EXCEPTION_STACKTRACE = 'exception_stacktrace'


class Type(Enum):
    COMICS = 'comics'
    REBINDS = 'rebinds'


class Result(Enum):
    PROCESSING = 'processing'
    SUCCESS = 'success'
    ERROR = 'error'


class Scan:
    def __init__(self, scan_type: Type):
        self._type: Type = scan_type
        self._result: Result = Result.PROCESSING
        self._started: datetime = datetime.utcnow()
        self._finished = None
        self._elapsed: str = ''
        self._scanned: int = 0
        self._skipped: int = 0
        self._added: int = 0
        self._updated: int = 0
        self._details: dict = {}
        self._exception_type = None
        self._exception_message = None
        self._exception_stacktrace = None

    @property
    def type(self) -> str:
        return self._type.value

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
    def scanned(self) -> int:
        return self._scanned

    @property
    def skipped(self) -> int:
        return self._skipped

    @property
    def added(self) -> int:
        return self._added

    @property
    def updated(self) -> int:
        return self._updated

    @property
    def details(self) -> dict:
        return self._details

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
        self._finished: datetime = datetime.utcnow()
        self._elapsed = str(self._finished - self._started)

    def inc_scanned(self, scanned: int):
        self._scanned += scanned

    def inc_skipped(self, skipped: int):
        self._skipped += skipped

    def inc_added(self, added: int):
        self._added += added

    def inc_updated(self, updated: int):
        self._updated += updated

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
            Property.TYPE.value: self._type.value,
            Property.RESULT.value: self._result.value,
            Property.STARTED.value: self.started_str,
            Property.FINISHED.value: self.finished_str,
            Property.ELAPSED.value: self._elapsed,
            Property.SCANNED.value: self._scanned,
            Property.SKIPPED.value: self._skipped,
            Property.ADDED.value: self._added,
            Property.UPDATED.value: self._updated,
            Property.DETAILS.value: self._details
        }
        if self._exception_type:
            json[Property.EXCEPTION_TYPE.value] = self._exception_type
        if self._exception_message:
            json[Property.EXCEPTION_MESSAGE.value] = self._exception_message
        if self._exception_stacktrace:
            json[Property.EXCEPTION_STACKTRACE.value] = self._exception_stacktrace
        return json

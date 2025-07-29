import os

logs = os.environ.get('logs', None)
print_logs: bool = bool(int(logs)) if logs else False


def info(message: str) -> None:
    if print_logs:
        print(message)

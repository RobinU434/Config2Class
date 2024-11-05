import logging
from watchdog.events import FileSystemEventHandler


class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path

    def on_modified(self, event):
        if event.src_path == self.file_path:
            print(f"The file '{self.file_path}' has been modified.")


def _observer_callback():
    logging.info("Hello")
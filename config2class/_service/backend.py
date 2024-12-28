import sys
import time
from config2class._core.constructor import ConfigConstructor
import config2class._utils.filesystem as fs_utils
from watchdog.events import FileSystemEventHandler, FileModifiedEvent
from watchdog.observers import Observer
import logging 
from typing import Any, Callable, Dict


class ConfigHandler(FileSystemEventHandler):
    def __init__(self, input_file: str, output_file: str = "config"):
        super().__init__()

        self.input_file = input_file
        self.output_file = output_file
        self.config_constructor = ConfigConstructor()
        self._load_func = self._get_load_func(self.input_file)
        try:
            ending = self.input_file.split(".")[-1]
            self._load_func = getattr(fs_utils, "load_" + ending)
        except AttributeError as error:
            raise NotImplementedError(
                f"Files with ending {ending} are not supported yet. Please use .yaml or .json or .toml."
            ) from error

    def on_modified(self, event: FileModifiedEvent):
        """
        Event handler triggered when the monitored file is modified. Logs the change and
        triggers a configuration update.

        Args:
            event (FileModifiedEvent): The event object containing information about the file change.
        """
        # print("modified: ", type(event), event.src_path)
        if event.src_path == self.input_file:
            logging.info(f"The file '{self.input_file}' has been modified.")
            self._create_config()

    @staticmethod
    def _get_load_func(input_file: str) -> Callable[[str], Dict[str, Any]]:
        try:
            ending = input_file.split(".")[-1]
            return getattr(fs_utils, "load_" + ending)
        except AttributeError as error:
            raise NotImplementedError(
                f"Files with ending {ending} are not supported yet. Please use .yaml or .json or .toml."
            ) from error

    def _create_config(self):
        """
        Loads content from the input file, constructs a configuration using
        `ConfigConstructor`, and writes the result to the output file.

        Raises:
            NotImplementedError: If the file type is not supported.
        """
        content = self._load_func(self.input_file)
        self.config_constructor.construct(content)
        self.config_constructor.write(self.output_file)
        logging.info(f"New config written to {self.output_file}")


def start_observer(input_file: str, output_file: str = "config.py"):
    # Create an event handler and an observer
    event_handler = ConfigHandler(input_file=input_file, output_file=output_file)
    observer = Observer()
    observer.schedule(event_handler, input_file, recursive=True)

    # Start the observer as a daemon thread
    # observer.daemon = True
    observer.start()

    print(f"Started observing {input_file}")

    # Keep running until the stop_event is set
    while True:
        time.sleep(2)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python backend.py <input-file> <output-file>")
        sys.exit(1)
    start_observer(*sys.argv[1:])
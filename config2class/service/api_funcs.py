import logging
import os
import threading
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from config2class.constructor import ConfigConstructor
from config2class.service.pid_coordination import add_pid, read_pid_file, remove_pid
import config2class.utils.filesystem as fs_utils

SHUTDOWN_FLAG = threading.Event()


class ServiceCallback(FileSystemEventHandler):
    """
    A callback class that observes file modifications and updates a configuration file
    based on changes to the observed file. Uses `watchdog` to monitor file events.

    Attributes:
        input (str): The path to the file being monitored for changes.
        output (str): The output file to which constructed configurations are saved.
        freq (int): The frequency (times per second) at which the observer checks for shutdown signals.
    """

    def __init__(self, input: str, output: str = "config.py", freq: int = 5):
        """
        Initializes the ServiceCallback with an input file path, output file path, and frequency.

        Args:
            input (str): The path to the file to be monitored for changes.
            output (str): The path to the output file for saving generated configurations.
            freq (int): Frequency to check for shutdown signals, in checks per second.
        """
        self.input = input
        self.output = output
        self.freq = freq

        self.config_constructor = ConfigConstructor()
        self.file_observer = Observer()
        self.file_observer.schedule(self, path=os.path.dirname(input), recursive=False)

    def _create_config(self):
        """
        Loads content from the input file, constructs a configuration using
        `ConfigConstructor`, and writes the result to the output file.

        Raises:
            NotImplementedError: If the file type is not supported.
        """
        try:
            ending = self.input.split(".")[-1]
            load_func = getattr(fs_utils, "load_" + ending)
        except AttributeError as error:
            raise NotImplementedError(
                f"Files with ending {ending} are not supported yet. Please use .yaml or .json or .toml."
            ) from error
        content = load_func(self.input)
        self.config_constructor.construct(content)
        self.config_constructor.write(self.output)

    def on_modified(self, event):
        """
        Event handler triggered when the monitored file is modified. Logs the change and
        triggers a configuration update.

        Args:
            event: The event object containing information about the file change.
        """
        if event.src_path == self.input:
            logging.info(f"The file '{self.input}' has been modified.")
            self._create_config()

    def __call__(self, *args, **kwds):
        """
        Starts the file observer and continuously monitors the input file for changes,
        checking periodically if the shutdown flag has been set. When the shutdown flag
        is set, stops the observer and exits gracefully.
        """
        # Loop until shutdown_flag is set to 1
        self.file_observer.start()

        while not SHUTDOWN_FLAG.is_set():
            time.sleep(1 / self.freq)

        logging.info("Background task is stopping gracefully.")
        self.file_observer.stop()
        self.file_observer.join()
        logging.info("Done")


def start_observer(input: str, output: str = "config.py"):
    """
    Starts a new background thread to observe changes to the input file and update the output configuration file.
    Logs the start of the process, creates a PID record, and sets up logging.

    Args:
        input (str): Path to the file to observe.
        output (str): Path to the configuration output file.

    Returns:
        threading.Thread: The started thread running the observer service.
    """
    target = ServiceCallback(input, output)
    # Start the background task as a separate process
    thread = threading.Thread(target=target, daemon=True)
    thread.start()
    # to keep track of running processes
    add_pid(thread.ident)

    # create a log file
    logging.basicConfig(
        filename=f"data/service_{thread.ident}.log",
        filemode="a",
        format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
        datefmt="%H:%M:%S",
        level=logging.DEBUG,
    )
    msg = f"Process started with PID {thread.ident}"
    logging.info(msg)
    print(msg)
    return thread


def stop_process(pid: int):
    """
    Stops the background observer thread associated with the specified PID by setting the shutdown flag.
    Verifies if the PID is actively running, then signals the shutdown and removes the PID from tracking.

    Args:
        pid (int): The process ID of the thread to be stopped.

    Logs:
        Warnings if the PID is not found, and informational messages during shutdown.
    """
    all_pids = read_pid_file()
    if pid not in all_pids:
        logging.warning("No running process found.")
        return

    SHUTDOWN_FLAG.set()
    logging.info("Shutdown flag set. Process will stop shortly.")
    time.sleep(1)
    remove_pid(pid)
    logging.info(f"Process stopped and removed PID={pid} from file.")

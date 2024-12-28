import logging
import os
import signal
import subprocess
import sys
import threading
import time
from pathlib import Path
from typing import Any, Callable, Dict
from watchdog.events import FileSystemEventHandler, FileModifiedEvent
from watchdog.observers import Observer

from config2class._core.constructor import ConfigConstructor
from config2class._service.backend import start_observer
from config2class._service.config import PID_FILE
from config2class._service.pid_coordination import add_pid, check_for_process, read_pid_file, remove_pid
import config2class._utils.filesystem as fs_utils



def start_service(input_file: str, output_file: str = "config.py", verbose: bool = False):
    """
    Starts a new background thread to observe changes to the input file and update the output configuration file.
    Logs the start of the process, creates a PID record, and sets up logging.

    Args:
        input_file (str): Path to the file to observe.
        output_file (str): Path to the configuration output file.
        verbose (bool, optional): if you want to print logs to terminal
    Returns:
        threading.Thread: The started thread running the observer service.
    """
    if not os.path.exists(PID_FILE):
        Path(PID_FILE).touch()
    if not os.path.exists(input_file):
        print(f"Input file does not exist: {input_file}")
        return
    if not os.path.exists(output_file):
        print(f"Output file does not exist: {output_file}")
        return
    print(__file__)
    if verbose:
        start_observer(input_file, output_file)
        return None
    
    check_for_process(input_file, output_file)
    # Start a new Python process that runs this script with an internal flag for `background_task`
    backend_file = "/".join([*__file__.split("/")[:-1], "backend.py"])
    process = subprocess.Popen(
        [sys.executable, backend_file, input_file, output_file],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        start_new_session=True,
    )  # Detach from the terminal
    add_pid(process.pid, input_file, output_file)

    print(f"Background process started with PID {process.pid}")
    return process.pid
    

def stop_process(pid: int):
    """
    Stops the background observer thread associated with the specified PID by setting the shutdown flag.
    Verifies if the PID is actively running, then signals the shutdown and removes the PID from tracking.

    Args:
        pid (int): The process ID of the thread to be stopped.

    Logs:
        Warnings if the PID is not found, and informational messages during shutdown.
    """
    # Check if the PID file exists
    remove_pid(pid)
    
    # Try to terminate the process using its PID
    try:
        os.kill(pid, signal.SIGTERM)
        print(f"Background process with PID {pid} stopped.")
    except ProcessLookupError:
        print(f"No process with PID {pid} found.")
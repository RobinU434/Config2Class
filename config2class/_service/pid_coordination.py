
import logging
import sys
from typing import Dict, Tuple
from config2class._utils import filesystem
from config2class._service.config import PID_FILE


def read_pid_file() -> Dict[int, Tuple[str, str]]:
    """
    Reads the PID file and returns a list of process IDs.

    Returns:
        Dict[str, Any]: Mapping from PID to observed files
    """
    content = filesystem.get_load_func(PID_FILE)(PID_FILE)
    return content

def check_for_process(input_file: str, output_file: str):
    content = read_pid_file()
    if content is None:
        return
    value = [input_file, output_file]
    if value in content.values():
        content_rev = {tuple(v): k for k, v in content.items()}
        msg = f"There is already a process (pid: {content_rev[tuple(value)]}) which maps from {input_file} to {output_file}"
        logging.error(msg)
        sys.exit()
    

def add_pid(pid: int, input_file: str, output_file: str):
    """
    Appends a new process ID to the PID file.

    Args:
        pid (int): The process ID to be added.
        input_file (str): input file of the process
        output_file (str): ouput file of the process
    """
    content = read_pid_file()
    if content is None:
        content = {}
    check_for_process(input_file, output_file)
    value = [input_file, output_file]
    content[pid] = value
    filesystem.get_write_func(PID_FILE)(PID_FILE, content)


def remove_pid(pid: int):
    """
    Removes a specific process ID from the PID file.
    If the PID is not found, the function exits without modifying the file.

    Args:
        pid (int): The process ID to be removed.
    """
    content = read_pid_file()
    try:
        content.pop(pid)
        filesystem.get_write_func(PID_FILE)(PID_FILE, content)
    except KeyError:
        msg = f"No logged running process with {pid=} found"
        logging.warning(msg)


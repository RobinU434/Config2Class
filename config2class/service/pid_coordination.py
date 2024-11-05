from typing import List, Literal

from config2class.service.config import PID_FILE


def read_pid_file() -> List[int]:
    """
    Reads the PID file and returns a list of process IDs.

    Returns:
        List[int]: A list of process IDs (integers) read from the PID file.
    """
    with open(PID_FILE, "r", encoding="utf-8") as f:
        all_pids = f.readlines()
    # convert to ints
    all_pids = list(map(lambda x: int(x.strip().rstrip("\n")), all_pids))
    return all_pids


def add_pid(pid: int):
    """
    Appends a new process ID to the PID file.

    Args:
        pid (int): The process ID to be added.
    """
    with open(PID_FILE, "a", encoding="utf-8") as f:
        f.write(str(pid) + "\n")


def overwrite_pid(pid: List[int]):
    """
    Overwrites the PID file with a new list of process IDs, replacing any existing content.

    Args:
        pid (List[int]): A list of process IDs to write to the PID file.
    """
    pid = list(map(lambda x: str(x) + "\n", pid))
    with open(PID_FILE, "w", encoding="utf-8") as f:
        f.writelines(pid)


def remove_pid(pid: int):
    """
    Removes a specific process ID from the PID file.
    If the PID is not found, the function exits without modifying the file.

    Args:
        pid (int): The process ID to be removed.
    """
    content = read_pid_file()
    try:
        content.pop(content.index(pid))
    except ValueError:
        return
    overwrite_pid(content)

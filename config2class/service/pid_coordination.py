from typing import List, Literal

from config2class.service.config import PID_FILE


def read_pid_file() -> List[int]:
    with open(PID_FILE, "r", encoding="utf-8") as f:
        all_pids = f.readlines()
    # convert to ints
    all_pids = list(map(lambda x: int(x.strip().rstrip("\n")), all_pids))
    return all_pids


def add_pid(pid: int):
    with open(PID_FILE, "a", encoding="utf-8") as f:
        f.write(str(pid) + "\n")


def overwrite_pid(pid: List[int]):
    pid = list(map(lambda x: str(x)+"\n", pid))
    with open(PID_FILE, "w", encoding="utf-8") as f:
        f.writelines(pid)


def remove_pid(pid: int):
    content = read_pid_file()
    try:
        content.pop(content.index(pid))
    except ValueError:
        return
    overwrite_pid(content)

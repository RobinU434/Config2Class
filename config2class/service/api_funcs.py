import logging
import multiprocessing
import os
import time
import signal
from typing import List
from watchdog.observers import Observer

from config2class.service.config import PID_FILE
from config2class.service.pid_coordination import add_pid, read_pid_file, remove_pid
from config2class.service.handler import FileChangeHandler, _observer_callback
import threading


# 'b' is for byte, 0 = running, 1 = shutdown
shutdown_flag = threading.Event()


def start_observer(file_path: str):
    def inner():
        msg = f"Background task started with PID {multiprocessing.current_process().pid}"
        logging.info(msg)

        # Loop until shutdown_flag is set to 1
        while not shutdown_flag.is_set():
            _observer_callback()
            time.sleep(0.2)

        logging.info("Background task is stopping gracefully.")


    # Start the background task as a separate process
    thread = threading.Thread(target=inner, daemon=True)
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
    all_pids = read_pid_file()
    if pid not in all_pids:
        logging.warning("No running process found.")
        return

    shutdown_flag.set()
    logging.info("Shutdown flag set. Process will stop shortly.")
    time.sleep(1)
    remove_pid(pid)
    logging.info(f"Process stopped and removed PID={pid} from file.")

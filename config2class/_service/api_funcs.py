import os
import signal
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable, Dict, List

from config2class._core.constructor import ConfigConstructor
from config2class._service.backend import start_observer
from config2class._service.config import PID_FILE
from config2class._service.pid_coordination import (
    add_pid,
    check_for_process,
    remove_pid,
)
from omegaconf import OmegaConf
import config2class.utils.filesystem as fs_utils
from hydra import compose, initialize
from hydra.errors import HydraException


def file2code(
    in_file_path: str,
    out_file_path: str = "config.py",
    init_none: bool = False,
    resolve: bool = False,
    ignore: List[str] = None,
):
    ending = in_file_path.split(".")[-1]
    try:
        load_func = getattr(fs_utils, "load_" + ending)
        load_func: Callable[[str], Dict[str, Any]]
    except AttributeError as error:
        raise NotImplementedError(
            f"Files with ending {ending} are not supported yet. Please use .yaml or .json or .toml."
        ) from error

    content = load_func(in_file_path)

    if resolve:
        # resolve expressions in config
        content = OmegaConf.create(content)
        content = OmegaConf.to_container(content, resolve=True)

    constructor = ConfigConstructor(ignore=ignore)
    constructor.construct(content)
    constructor.write(out_file_path, init_none)


def hydra2code(
    in_file_path: str,
    out_file_path: str = "config.py",
    init_none: bool = False,
    resolve: bool = False,
):
    """_summary_

    Args:
        in_file_path (str): _description_
        out_file_path (str, optional): _description_. Defaults to "config.py".
        init_none (bool, optional): _description_. Defaults to False.
        resolve (bool, optional): _description_. Defaults to False.

    """
    in_file_path: Path = Path(in_file_path)
    if in_file_path.is_absolute():
        call_dir = Path()
        # change to relative path from system root
        in_file_path = Path(str(in_file_path)[1:])
    else:
        # change to relative path from system root
        call_dir = Path(str(Path.cwd())[1:])

    # move relative from from file dire to system root to call dir to specified input file
    file_dir = Path(__file__).parent
    cd_path = Path().joinpath(*[".." for _ in file_dir.parents])

    in_file_path = cd_path.joinpath(call_dir).joinpath(in_file_path)

    config_path = str(in_file_path.parent)
    config_name = str(in_file_path.stem)
    with initialize(version_base=None, config_path=config_path, job_name=None):
        cfg = compose(config_name=config_name)

    content = OmegaConf.to_container(cfg, resolve=resolve)
    constructor = ConfigConstructor()
    constructor.construct(content)
    constructor.write(out_file_path, init_none)


def start_service(
    input_file: str,
    output_file: str = "config.py",
    verbose: bool = False,
    init_none: bool = False,
):
    """
    Starts a new background thread to observe changes to the input file and update the output configuration file.
    Logs the start of the process, creates a PID record, and sets up logging.

    Args:
        input_file (str): Path to the file to observe.
        output_file (str): Path to the configuration output file.
        verbose (bool, optional): if you want to print logs to terminal
        init_none (bool, optional): Would you like to init all argument with None or just declare members in the class. Defaults to False
    Returns:
        threading.Thread: The started thread running the observer service.
    """
    if not os.path.exists(PID_FILE):
        path = Path(PID_FILE)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch(exist_ok=True)
    if not os.path.exists(input_file):
        print(f"Input file does not exist: {input_file}")
        return
    if not os.path.exists(output_file):
        print(f"Output file does not exist: {output_file}")

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

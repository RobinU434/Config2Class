from pathlib import Path
from typing import Any, Callable, Dict, List
from omegaconf import OmegaConf
from config2class._service.api_funcs import (
    dir2code,
    hydra2code,
    file2code,
    start_service,
    stop_process,
)
from config2class._service.pid_coordination import read_pid_file
import config2class.utils.filesystem as fs_utils
from config2class._core.constructor import ConfigConstructor
from glob import glob
import os

from config2class.utils.logging import set_log_level_debug


class Config2Code:
    """
    Converts configuration data from a YAML or JSON file into a Python dataclass.

    This class facilitates automatic generation of dataclasses from configuration
    files. It currently supports YAML and JSON file formats.
    """

    def __init__(self):
        """
        Initializes a new `Config2Code` instance.
        """
        pass

    def file2code(
        self,
        input: str,
        output: str = "config.py",
        init_none: bool = False,
        resolve: bool = False,
        ignore: List[str] = None,
        verbose: bool = False,
    ):
        """
        Converts a configuration file to a Python dataclass and writes the code to a file.

        Args:
            input (str): The path to the configuration file (YAML or JSON).
            output (str, optional): The path to the output file where the generated
                dataclass code will be written. Defaults to "config.py".
            init_none (bool, optional): Would you like to init all argument with None or just declare members in the class. Defaults to False
            resolve: (bool, optional): Set this flag to resolve expressions in the loaded config. Defaults to False
            ignore: (List[str], optional): ignore element from config. To point to certain element in the config you would use point notation. Defaults to None.
            verbose: (bool, optional): Set log level to logging.DEBUG. Defaults to False
        Raises:
            NotImplementedError: If the input file format is not YAML or JSON or TOML.
        """
        if verbose:
            set_log_level_debug()
        file2code(input, output, init_none, resolve, ignore)

    def dir2code(
        self,
        input: str,
        output: str = ".",
        recursive: bool = False,
        init_none: bool = False,
        resolve: bool = False,
        verbose: bool = False,
        prefix: str = "",
        suffix: str = "_config",
    ):
        """Convert all config files in a directory into a structured config.

        Args:

            input (str): The path to the directories with config file (YAML or JSON).
            output (str, optional): The path to the output directory where the generated
                dataclass code will be written. Defaults to ".".
            recursive (bool, optional): If set look for all nested config files. Defaults to False.
            init_none (bool, optional): Would you like to init all argument with None or just declare members in the class. Defaults to False
            resolve: (bool, optional): Set this flag to resolve expressions in the loaded config. Defaults to False
            verbose: (bool, optional): Set log level to logging.DEBUG. Defaults to False
            prefix (str, optional): prefix for output file name. Defaults to "".
            suffix (str, optional): prefix for output file name. Defaults to "_config".
        """
        if verbose:
            set_log_level_debug()
        dir2code(
            input,
            output,
            recursive,
            init_none,
            resolve,
            prefix,
            suffix,
        )

    def hydra2code(
        self,
        input: str,
        output: str = "config.py",
        init_none: bool = False,
        resolve: bool = False,
        verbose: bool = False,
    ):
        """converts a hydra config into a structured config

        Args:
            input (str): The path to the configuration file (YAML or JSON).
            output (str, optional): The path to the output file where the generated
                dataclass code will be written. Defaults to "config.py".
            init_none (bool, optional): Would you like to init all argument with None or just declare members in the class. Defaults to False
            resolve: (bool, optional): Set this flag to resolve expressions in the loaded config. Defaults to False
            verbose: (bool, optional): Set log level to logging.DEBUG. Defaults to False
        """
        if verbose:
            set_log_level_debug()
        hydra2code(input, output, init_none, resolve)

    def start_service(
        self,
        input: str,
        output: str = "config.py",
        verbose: bool = False,
        init_none: bool = False,
    ):
        """start an observer to create the config automatically.

        Args:
            input (str): input file you want to have observed
            output (str, optional): python file to write the dataclasses in. Defaults to "config.py".
            verbose (bool, optional): if you want to print logs to terminal
            init_none (bool, optional): Would you like to init all argument with None or just declare members in the class. Defaults to False
        """
        start_service(input, output, verbose, init_none)

    def stop_service(self, pid: int):
        """stop a particular service

        Args:
            pid (int): process id
        """
        stop_process(pid)

    def stop_all(self):
        """stop all services"""
        for pid in read_pid_file():
            self.stop_service(pid)

    def list_services(self):
        """print currently running processes"""
        for pid, (input_file, output_file) in read_pid_file().items():
            print(f"{pid}: {input_file} -> {output_file}")

    def clear_logs(self):
        """delete all log files"""
        for file_name in glob("data/*.logs"):
            os.remove(file_name)

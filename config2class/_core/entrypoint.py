from config2class._service.api_funcs import read_pid_file, start_service, stop_process
import config2class._utils.filesystem as fs_utils
from config2class._core.constructor import ConfigConstructor
from glob import glob
import os


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

    def to_code(self, input: str, output: str = "config.py"):
        """
        Converts a configuration file to a Python dataclass and writes the code to a file.

        Args:
            input (str): The path to the configuration file (YAML or JSON).
            output (str, optional): The path to the output file where the generated
                dataclass code will be written. Defaults to "config.py".

        Raises:
            NotImplementedError: If the input file format is not YAML or JSON or TOML.
        """
        try:
            ending = input.split(".")[-1]
            load_func = getattr(fs_utils, "load_" + ending)
        except AttributeError as error:
            raise NotImplementedError(
                f"Files with ending {ending} are not supported yet. Please use .yaml or .json or .toml."
            ) from error

        content = load_func(input)
        constructor = ConfigConstructor()
        constructor.construct(content)
        constructor.write(output)

    def start_service(
        self, input: str, output: str = "config.py", verbose: bool = False
    ):
        """start an observer to create the config automatically.

        Args:
            input (str): input file you want to have observed
            output (str, optional): python file to write the dataclasses in. Defaults to "config.py".
            verbose (bool, optional): if you want to print logs to terminal
        """
        start_service(input, output, verbose)

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

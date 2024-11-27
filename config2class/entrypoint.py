from config2class.service.api_funcs import read_pid_file, start_service, stop_process
import config2class.utils.filesystem as fs_utils
from config2class.constructor import ConfigConstructor
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

    def to_code(self, inpath=str, outpath: str|None = None):
        """
        Converts a configuration file to a Python dataclass and writes the code to a file.
        If target is a folder, applied recursively to all applicable files inside.

        Args:
            inpath (str): The path to the configuration file (YAML/JSON/TOML) or folder. 
            output (str, optional): The path to the output file/folder where the generated
                dataclass will be written. Defaults to config.py / pyconfig_dir.
        """
        if os.path.isdir(inpath):
            return self.to_code_multiple(inpath=inpath, outpath=outpath)
        else:
            return self.to_code_single(input=inpath, output=outpath)


    def to_code_multiple(self, inpath=str, outpath: str|None = None):
        """
        Convert a folder of configuration files to a similar of folder of dataclasses.

        Args:
            inpath (str): The path to the configuration folder. 
            output (str, optional): The path to the output file/folder where the generated
                dataclass will be written. Defaults to pyconfig_dir.
        """
        inpath = os.path.abspath(inpath)
        outpath = outpath or os.path.join(os.path.dirname(inpath), "pyconfig_dir")
        # parse
        for root, dirs, files in os.walk(inpath):
            # record relative path
            relpath = os.path.relpath(root, inpath)

            for dir_name in dirs:
                new_dir = os.path.normpath(os.path.join(outpath, relpath, dir_name))
                os.makedirs(new_dir, exist_ok=True)

            for file_name in files:
                if os.path.splitext(file_name)[1] not in [".yaml", ".toml", ".json"]: # supported extension should be a constant
                    continue

                orig_name = os.path.splitext(file_name)[0] 
                new_name = os.path.normpath(os.path.join(outpath, relpath, orig_name+ ".py"))
                self.to_code_single(input=os.path.join(root, file_name), output=new_name)




    def to_code_single(self, input: str, output: str|None = None):
        """
        Converts a configuration file to a Python dataclass and writes the code to a file.

        Args:
            input (str): The path to the configuration file (YAML or JSON).
            output (str, optional): The path to the output file where the generated
                dataclass code will be written. Defaults to "config.py".

        Raises:
            NotImplementedError: If the input file format is not YAML or JSON or TOML.
        """
        output = output or "config.py"
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

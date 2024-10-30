import config2class.utils.filesystem as fs_utils
from config2class.constructor import ConfigConstructor


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

    def to_code(self, input_file: str, out_file: str = "config.py"):
        """
        Converts a configuration file to a Python dataclass and writes the code to a file.

        Args:
            input_file (str): The path to the configuration file (YAML or JSON).
            out_file (str, optional): The path to the output file where the generated
                dataclass code will be written. Defaults to "config.py".

        Raises:
            NotImplementedError: If the input file format is not YAML or JSON or TOML.
        """
        try:
            ending = input_file.split(".")[-1]
            load_func = getattr(fs_utils, "load_" + ending)
        except AttributeError as error:
            raise NotImplementedError(
                f"Files with ending {ending} are not supported yet. Please use .yaml or .json or .toml."
            ) from error

        content = load_func(input_file)
        constructor = ConfigConstructor()
        constructor.construct(content)
        constructor.write(out_file)

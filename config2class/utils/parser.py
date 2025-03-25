from argparse import ArgumentParser
from typing import Tuple, Dict, List


def add_clear_logs_args(parser: ArgumentParser) -> ArgumentParser:
    return parser


def add_list_services_args(parser: ArgumentParser) -> ArgumentParser:
    return parser


def add_stop_all_args(parser: ArgumentParser) -> ArgumentParser:
    return parser


def add_stop_service_args(parser: ArgumentParser) -> ArgumentParser:
    parser.add_argument(
        "--pid",
        help="process id",
        dest="pid",
        type=int,
        required=True,
    )
    return parser


def add_start_service_args(parser: ArgumentParser) -> ArgumentParser:
    parser.add_argument(
        "--input",
        help="input file you want to have observed",
        dest="input",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--output",
        help='python file to write the dataclasses in. Defaults to "config.py".',
        dest="output",
        type=str,
        default="config.py",
        required=False,
    )
    parser.add_argument(
        "--verbose",
        help="if you want to print logs to terminal",
        dest="verbose",
        action="store_true",
        required=False,
    )
    parser.add_argument(
        "--init-none",
        help="Would you like to init all argument with None or just declare members in the class. Defaults to False",
        dest="init_none",
        action="store_true",
        required=False,
    )
    return parser


def add_hydra2code_args(parser: ArgumentParser) -> ArgumentParser:
    parser.add_argument(
        "--input",
        help="The path to the configuration file (YAML or JSON).",
        dest="input",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--output",
        help="The path to the output file where the generated",
        dest="output",
        type=str,
        default="config.py",
        required=False,
    )
    parser.add_argument(
        "--init-none",
        help="",
        dest="init_none",
        action="store_true",
        required=False,
    )
    parser.add_argument(
        "--resolve",
        help="Would you like to init all argument with None or just declare members in the class. Defaults to False",
        dest="resolve",
        action="store_true",
        required=False,
    )
    parser.add_argument(
        "--verbose",
        help="(bool, optional): Set this flag to resolve expressions in the loaded config. Defaults to False",
        dest="verbose",
        action="store_true",
        required=False,
    )
    return parser


def add_dir2code_args(parser: ArgumentParser) -> ArgumentParser:
    parser.add_argument(
        "--input",
        help="--no-documentation-exists--",
        dest="input",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--output",
        help="--no-documentation-exists--",
        dest="output",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--recursive",
        help="--no-documentation-exists--",
        dest="recursive",
        action="store_true",
        required=False,
    )
    parser.add_argument(
        "--init-none",
        help="--no-documentation-exists--",
        dest="init_none",
        action="store_true",
        required=False,
    )
    parser.add_argument(
        "--resolve",
        help="--no-documentation-exists--",
        dest="resolve",
        action="store_true",
        required=False,
    )
    parser.add_argument(
        "--verbose",
        help="--no-documentation-exists--",
        dest="verbose",
        action="store_true",
        required=False,
    )
    parser.add_argument(
        "--prefix",
        help="--no-documentation-exists--",
        dest="prefix",
        type=str,
        default="",
        required=False,
    )
    parser.add_argument(
        "--suffix",
        help="--no-documentation-exists--",
        dest="suffix",
        type=str,
        default="_config",
        required=False,
    )
    parser.add_argument(
        "--flatten",
        help="--no-documentation-exists--",
        dest="flatten",
        action="store_true",
        required=False,
    )
    return parser


def add_file2code_args(parser: ArgumentParser) -> ArgumentParser:
    parser.add_argument(
        "--input",
        help="The path to the configuration file (YAML or JSON).",
        dest="input",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--output",
        help="The path to the output file where the generated",
        dest="output",
        type=str,
        default="config.py",
        required=False,
    )
    parser.add_argument(
        "--init-none",
        help="",
        dest="init_none",
        action="store_true",
        required=False,
    )
    parser.add_argument(
        "--resolve",
        help="Would you like to init all argument with None or just declare members in the class. Defaults to False",
        dest="resolve",
        action="store_true",
        required=False,
    )
    parser.add_argument(
        "--ignore",
        help="(bool, optional): Set this flag to resolve expressions in the loaded config. Defaults to False",
        dest="ignore",
        type=str,
        nargs="+",
        default=None,
        required=False,
    )
    parser.add_argument(
        "--verbose",
        help="(List[str], optional): ignore element from config. To point to certain element in the config you would use point notation. Defaults to None.",
        dest="verbose",
        action="store_true",
        required=False,
    )
    return parser


def setup_config2code_parser(
    parser: ArgumentParser,
) -> Tuple[ArgumentParser, Dict[str, ArgumentParser]]:
    subparser = {}
    command_subparser = parser.add_subparsers(dest="command", title="command")
    file2code = command_subparser.add_parser(
        "file2code",
        help="Converts a configuration file to a Python dataclass and writes the code to a file.",
    )
    file2code = add_file2code_args(file2code)
    subparser["file2code"] = file2code
    dir2code = command_subparser.add_parser(
        "dir2code", help="--no-documentation-exists--"
    )
    dir2code = add_dir2code_args(dir2code)
    subparser["dir2code"] = dir2code
    hydra2code = command_subparser.add_parser(
        "hydra2code", help="converts a hydra config into a structured config"
    )
    hydra2code = add_hydra2code_args(hydra2code)
    subparser["hydra2code"] = hydra2code
    start_service = command_subparser.add_parser(
        "start-service", help="start an observer to create the config automatically."
    )
    start_service = add_start_service_args(start_service)
    subparser["start_service"] = start_service
    stop_service = command_subparser.add_parser(
        "stop-service", help="stop a particular service"
    )
    stop_service = add_stop_service_args(stop_service)
    subparser["stop_service"] = stop_service
    stop_all = command_subparser.add_parser("stop-all", help="stop all services")
    stop_all = add_stop_all_args(stop_all)
    subparser["stop_all"] = stop_all
    list_services = command_subparser.add_parser(
        "list-services", help="print currently running processes"
    )
    list_services = add_list_services_args(list_services)
    subparser["list_services"] = list_services
    clear_logs = command_subparser.add_parser("clear-logs", help="delete all log files")
    clear_logs = add_clear_logs_args(clear_logs)
    subparser["clear_logs"] = clear_logs
    return parser, subparser


def setup_parser(parser: ArgumentParser) -> ArgumentParser:
    parser, _ = setup_config2code_parser(parser)
    return parser

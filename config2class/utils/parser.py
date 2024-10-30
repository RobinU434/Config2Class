from argparse import ArgumentParser


def add_to_code_args(parser: ArgumentParser) -> ArgumentParser:
    parser.add_argument(
        "--input",
        help="The path to the configuration file (YAML or JSON).",
        dest="input",
        type=str,
    )
    parser.add_argument(
        "--output",
        help="The path to the output file where the generated",
        dest="output",
        type=str,
        default="config.py",
    )
    return parser


def setup_config2code_parser(parser: ArgumentParser) -> ArgumentParser:
    command_subparser = parser.add_subparsers(dest="command", title="command")
    to_code = command_subparser.add_parser(
        "to-code",
        help="Converts a configuration file to a Python dataclass and writes the code to a file.",
    )
    to_code = add_to_code_args(to_code)
    return parser


def setup_parser(parser: ArgumentParser) -> ArgumentParser:
    parser = setup_config2code_parser(parser)
    return parser

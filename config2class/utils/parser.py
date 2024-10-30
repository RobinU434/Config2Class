from argparse import ArgumentParser


def add_to_code_args(parser: ArgumentParser) -> ArgumentParser:
    parser.add_argument(
        "--input-file",
        help="config file to convert to dataclasses",
        dest="input_file",
        type=str,
    )
    parser.add_argument(
        "--out-file",
        help="where to put out the generated code",
        dest="out_file",
        type=str,
        default="config.py",
    )
    return parser


def setup_config2code_parser(parser: ArgumentParser) -> ArgumentParser:
    command_subparser = parser.add_subparsers(dest="command", title="command")
    to_code = command_subparser.add_parser(
        "to-code", help="convert given config file into dataclasses. "
    )
    to_code = add_to_code_args(to_code)
    return parser


def setup_parser(parser: ArgumentParser) -> ArgumentParser:
    parser = setup_config2code_parser(parser)
    return parser

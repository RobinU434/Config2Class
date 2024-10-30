from argparse import ArgumentParser
from config2class.main import Config2Code
from config2class.utils.parser import setup_parser


def execute(args: dict) -> bool:
    module = Config2Code()
    match args["command"]:
        case "to-code":
            module.to_code(input_file=args["input_file"], out_file=args["out_file"])

        case _:
            return False

    return True


def create_parser() -> ArgumentParser:
    parser = ArgumentParser(description="Config to Code")

    parser = setup_parser(parser)

    return parser


def main() -> None:
    parser = create_parser()
    args = parser.parse_args()
    args_dict = vars(args)
    if not execute(args_dict):
        parser.print_usage()


if __name__ == "__main__":
    main()

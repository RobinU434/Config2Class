from argparse import ArgumentParser
from pathlib import Path
from pyargwriter import api
from config2class.utils.parser import setup_config2code_parser
from config2class._core.entrypoint import Config2Code
from config2class.utils.parser import setup_parser


def execute(args: dict) -> bool:
    module = Config2Code()
    _, command_parser = setup_config2code_parser(ArgumentParser())
    match args["command"]:
        case "file2code":
            module.file2code(
                input=args["input"],
                output=args["output"],
                init_none=args["init_none"],
                resolve=args["resolve"],
                ignore=args["ignore"],
                verbose=args["verbose"],
            )

        case "dir2code":
            module.dir2code(
                input=args["input"],
                output=args["output"],
                recursive=args["recursive"],
                init_none=args["init_none"],
                resolve=args["resolve"],
                verbose=args["verbose"],
                prefix=args["prefix"],
                suffix=args["suffix"],
                flatten=args["flatten"],
            )

        case "hydra2code":
            module.hydra2code(
                input=args["input"],
                output=args["output"],
                init_none=args["init_none"],
                resolve=args["resolve"],
                verbose=args["verbose"],
            )

        case "start-service":
            module.start_service(
                input=args["input"],
                output=args["output"],
                verbose=args["verbose"],
                init_none=args["init_none"],
            )

        case "stop-service":
            module.stop_service(pid=args["pid"])

        case "stop-all":
            module.stop_all()

        case "list-services":
            module.list_services()

        case "clear-logs":
            module.clear_logs()

        case _:
            return False

    return True


def create_parser() -> ArgumentParser:
    parser = ArgumentParser(
        description="Converts configuration data from a YAML or JSON file into a Python dataclass."
    )

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

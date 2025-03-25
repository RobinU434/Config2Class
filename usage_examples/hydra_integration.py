import logging
from argparse import ArgumentParser
from omegaconf import DictConfig

from config2class.utils.parser import setup_parser
from config2class.api.hydra import hydra_wrapper
from usage_examples.config import App_config


def pseudo_train(cfg: DictConfig, device: str = "cpu"):
    """start pseudo training

    Args:
        cfg (Dict[str, Any]): _description_
        device (str, optional): _description_. Defaults to "cpu".
    """
    cfg: App_config = App_config.from_dict_config(cfg, resolve=True)
    print("start training with config")
    logging.info("start training with config")
    print(cfg.database.credentials.password)
    print("on device: ", device)


def main():
    parser = ArgumentParser()
    command_sub_parser = parser.add_subparsers(title="command", dest="command")
    train_parser = command_sub_parser.add_parser("train", add_help=False)

    train_parser = setup_parser(train_parser)
    train_parser.add_argument("--device", type=str, default="gpu")
    args = parser.parse_args()

    hydra_wrapper(
        pseudo_train,
        args,
        train_parser,
        config_path="example/",
        config_name="example.yaml",
        version_base=None,
    )


if __name__ == "__main__":
    main()

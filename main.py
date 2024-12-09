import abc
import ast
import functools
import inspect
import logging
from argparse import (
    Action,
    ArgumentParser,
    Namespace,
    _StoreAction,
    _StoreTrueAction,
    _VersionAction,
)
from collections import OrderedDict
from dataclasses import dataclass
import dataclasses
from textwrap import dedent
from time import time
from typing import Any, Dict

from hydra._internal.utils import _run_hydra, get_args_parser
from hydra._internal.deprecation_warning import deprecation_warning
from hydra.core.config_store import ConfigStore
from hydra.core.utils import _flush_loggers
from hydra.main import _get_rerun_conf, _UNSPECIFIED_
from hydra import version

from out import App_config

logger = logging.getLogger(__name__)


# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
# TODO: write a decorator which sets a flag with args where to deploy the decorator above
class Decorator(ast.NodeVisitor, abc.ABC):
    def __init__(self):
        super().__init__()
        self.decorator_args = OrderedDict()

    def visit_FunctionDef(self, node: ast.FunctionDef):
        # Look for decorators on the function
        for decorator in node.decorator_list:
            decorator: ast.Call
            # if not isinstance(decorator, ast.Call) or not hasattr(decorator.func, "id"):
            #     continue
            try:
                decorator_cls_name = decorator.func.value.id
            except AttributeError:
                continue

            if decorator_cls_name != type(self).__name__:
                continue

            # Extract explicitly provided args and kwargs
            args = [ast.literal_eval(arg) for arg in decorator.args]
            kwargs = {kw.arg: ast.literal_eval(kw.value) for kw in decorator.keywords}

            # Combine with defaults from the decorator signature
            final_args = self._merge_with_defaults(args, kwargs)
            self.decorator_args = {**self.decorator_args, **final_args}
        self.generic_visit(node)

    def _merge_with_defaults(self, args, kwargs):
        # Get the signature of the decorator function
        sig = inspect.signature(self.decorator)

        # Build a mapping of parameter names to their defaults
        params = sig.parameters
        default_values = {
            name: param.default
            for name, param in params.items()
            if param.default is not param.empty
        }

        # Match positional args to parameter names
        param_names = list(params.keys())
        for i, arg in enumerate(args):
            default_values[param_names[i]] = arg

        # Override with explicitly provided keyword arguments
        default_values.update(kwargs)

        return default_values

    @classmethod
    def decorator(self, *args, **kwargs):
        raise NotImplementedError

    @classmethod
    def deploy(self, *args, **kwargs):
        raise NotImplementedError


class AddHydra(Decorator):
    def __init__(
        self,
        hydra_args: Namespace,
        arg_parser: ArgumentParser,
        version_base: str = _UNSPECIFIED_,
        config_var_name: str = "config",
        config_path: str = _UNSPECIFIED_,
        config_name: str = None

    ):
        super().__init__()
        self.hydra_args = hydra_args
        self.arg_parser = arg_parser

        self.version_base = version_base
        self.config_var_name = config_var_name
        self.config_path = config_path
        self.config_name = config_name


        self.config_store = ConfigStore.instance()

    @classmethod
    def decorator(
        cls,
        version_base: str = _UNSPECIFIED_,
        config_var_name: str = "config",
        config_path: str = _UNSPECIFIED_,
        config_name: str = None
    ):
        """_summary_

        Args:
            version_base (str, optional): No idea. Defaults to None.
            config_var_name (str, optional): variable name which variable to insert the config to. Defaults to "config".
            config_path (str, optional): where to find the config -> default arg for hydra. Defaults to ".".
        """

        def add_hydra_decorator(func):
            @functools.wraps(func)
            def decorated_func_add_hydra(*args, **kwargs):
                func(*args, **kwargs)
                # raise NotImplementedError

            return decorated_func_add_hydra

        return add_hydra_decorator
    
    def _handle_struct_config(self, config_annotation):
        # NOTE: this is purely tuned for Config2Class config classes and not structured classes
        # It can maybe handle structured configs
        if dataclasses.is_dataclass(config_annotation):
            if self.hydra_args.config_name is None:
                raise ValueError("config_name can't be None for a structured config")
            h = str(hash(time()))

            if hasattr(config_annotation, "from_file"):
                structured_config = getattr(config_annotation, "from_file")(
                    self.hydra_args.config_name
                )
            else:
                structured_config = config_annotation

            self.config_store.store(name=h, node=structured_config)
            self.hydra_args.config_name = h


    def _prepare_hydra(self):
        version.setbase(self.version_base)

        if self.config_path is _UNSPECIFIED_:
            if version.base_at_least("1.2"):
                self.config_path = None
            elif self.version_base is _UNSPECIFIED_:
                url = "https://hydra.cc/docs/1.2/upgrades/1.0_to_1.1/changes_to_hydra_main_config_path"
                deprecation_warning(
                    message=dedent(
                        f"""
                    config_path is not specified in @hydra.main().
                    See {url} for more information."""
                    ),
                    stacklevel=2,
                )
                self.config_path = "."
            else:
                self.config_path = "."


    def deploy(self, task_function: callable, config_var_name: str):
        task_function_signature = inspect.signature(task_function, follow_wrapped=True)
        parameters = dict(task_function_signature.parameters)
        config_annotation = parameters.pop(config_var_name).annotation
        self._handle_struct_config(config_annotation)

        # extract re    maining parameters from arguments
        partial_args = {k: getattr(self.hydra_args, k) for k in parameters}

        self._prepare_hydra()

        if self.hydra_args.experimental_rerun is not None:
            cfg = _get_rerun_conf(
                self.hydra_args.experimental_run, self.hydra_args.overrides
            )
            task_function(**{config_var_name: cfg, **partial_args})
            _flush_loggers()
        else:
            # no return value from run_hydra() as it may sometime actually run the task_function
            # multiple times (--multirun)
            _run_hydra(
                args=self.hydra_args,
                args_parser=self.arg_parser,
                task_function=lambda config: task_function(
                    **{config_var_name: config, **partial_args}
                ),
                config_path=".",  # TODO set from init
                config_name="config",  # TODO: set from init
            )


# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<


@AddHydra.decorator(
    config_var_name="config",
    config_path=".",
)
def pseudo_train(config2: App_config, device: str = "cpu"):
    """start pseudo training

    Args:
        config (Dict[str, Any]): _description_
        device (str, optional): _description_. Defaults to "cpu".
    """
    print("start training with config")
    logging.info("start training with config")
    print(config2)
    print("on device: ", device)


def setup_parser(new_parser: ArgumentParser = None) -> ArgumentParser:
    if new_parser is None:
        new_parser = ArgumentParser(add_help=False)

    hydra_parser = get_args_parser()

    for action in hydra_parser._actions:
        action: Action
        option_strings = action.option_strings

        if len(option_strings) == 0:
            new_parser.add_argument(
                action.dest,
                nargs=action.nargs,
                help=action.help,
            )
        elif isinstance(action, _StoreAction):
            new_parser.add_argument(
                *option_strings,
                action="store",
                nargs=action.nargs,
                default=action.default,
                type=action.type,
                help=action.help,
                choices=action.choices,
            )
        elif isinstance(action, _StoreTrueAction):
            new_parser.add_argument(
                *option_strings,
                action="store_true",
                help=action.help,
            )
        elif isinstance(action, _VersionAction):
            new_parser.add_argument(
                "--hydra-version",
                action="version",
                help=action.help,
                version=action.version,
            )
        else:
            raise NotImplementedError
    return new_parser


def main():

    parser = ArgumentParser()
    command_sub_parser = parser.add_subparsers(title="command", dest="command")
    train_parser = command_sub_parser.add_parser("train", add_help=False)
    train_parser = setup_parser(train_parser)
    train_parser.add_argument("--device", type=str, default="gpu")
    args = parser.parse_args()

    decorator = AddHydra(args, train_parser, version_base=None)
    decorator.deploy(pseudo_train, "config2")


if __name__ == "__main__":
    main()

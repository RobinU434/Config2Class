from typing import Any, Dict

from config2class._utils.dict_operations import find_cycles, flatten_dict, unflatten
from config2class._utils.token_operations import (
    build_dependency_graph,
    get_token_content,
    is_token,
    token_in,
)


def replace_tokens(d: Dict[str, Any]) -> Dict[str, Any]:
    pattern = r"\{\{.*?\}\}"

    if len(d) == 0:
        return d

    nested = len(d) > 1
    prefix = "__CONFIG__"
    if nested:
        d = {prefix: d}
    d_flatten = flatten_dict(d)

    # check incoming dict
    res = {}
    for key, value in d_flatten.items():
        if not is_token(value, pattern):
            res[key] = value
            continue

        token_value = get_token_content(value)
        split = token_value.split(".")
        split = [ele.strip() for ele in split]
        if nested and len(split[0]) == 0 and len(split) > 1:
            split[0] = prefix
        if "" in split or [" "] == split:
            raise ValueError(f"token={value} is not valid")

        value = "{{" + ".".join(split) + "}}"
        res[key] = value
    d_flatten = res

    dependencies = build_dependency_graph(d)
    cycles = len(find_cycles(dependencies)) > 0
    if cycles:
        raise ValueError(
            f"The config file contains cycles is therefor not valid to parse. Cycle: {cycles}"
        )

    while token_in(d_flatten):
        for key, value in d_flatten.items():
            if not is_token(value, pattern):
                continue
            # strip from token
            try:
                d_flatten[key] = d_flatten[value.strip("{}")]
            except KeyError as error:
                raise ValueError(f"token={value} is not valid") from error
    res = unflatten(d_flatten)
    if nested:
        _, res = res.popitem()
    return res

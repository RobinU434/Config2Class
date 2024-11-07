from typing import Dict, List


def unflatten(d: Dict[str, str]) -> List[List[str]]:
    # from https://stackoverflow.com/questions/6037503/python-unflatten-dict
    resultDict = dict()
    for key, value in d.items():
        parts = key.split(".")
        d = resultDict
        for part in parts[:-1]:
            if part not in d:
                d[part] = dict()
            d = d[part]
        d[parts[-1]] = value
    return resultDict


def flatten_dict(d: dict):
    if d is None or len(d) == 0:
        return {}
    res = {}
    for key, value in d.items():
        if isinstance(value, dict):
            value = {key + "." + k: v for k, v in value.items()}
            res = {**res, **value}
            res = flatten_dict(res)
        else:
            res[key] = value
    return res


def find_cycles(graph):
    def visit(node, path, visited):
        if node in path:
            # Cycle detected; collect the cycle
            cycle_start_index = path.index(node)
            cycles.append(path[cycle_start_index:])
            return
        if node in visited:
            # Node already processed, skip
            return

        # Mark this node as visited and part of the current path
        visited.add(node)
        path.append(node)

        # Recurse to the next node if it exists
        if node in graph:
            next_node = graph[node]
            if next_node:  # There is an outgoing edge
                visit(next_node, path, visited)

        # Backtrack: remove the node from the current path
        path.pop()

    visited = set()
    cycles = []

    # Check each node in the graph
    for node in graph:
        if node not in visited:
            visit(node, [], visited)

    return cycles

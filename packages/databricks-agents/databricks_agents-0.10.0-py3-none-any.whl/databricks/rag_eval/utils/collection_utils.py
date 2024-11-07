"""Utilities for manipulating collections."""

from typing import Any, Dict, List, Mapping, Sequence


def omit_keys(d: Mapping[str, Any], keys: List[str]) -> Dict[str, Any]:
    """
    Omit keys from a dictionary.
    :param d:
    :param keys:
    :return: A new dictionary with the keys removed.
    """
    return {k: v for k, v in d.items() if k not in keys}


def position_map_to_list(d: Mapping[int, Any], default: Any = None) -> List[Any]:
    """
    Convert a position map to a list ordered by position. Missing positions are filled with the default value.
    Position starts from 0.

    e.g. {0: 'a', 1: 'b', 3: 'c'} -> ['a', 'b', default, 'c']

    :param d: A position map.
    :param default: The default value to fill missing positions.
    :return: A list of values in the map.
    """
    length = max(d.keys(), default=-1) + 1
    return [d.get(i, default) for i in range(length)]


def deep_update(original, updates):
    """
    Recursively update a dictionary with another dictionary.

    Example:
        deep_update({a: {b: 1}}, {a: {c: 2}})
        # Result: {a: {b: 1, c: 2}}

    :param original: The original dictionary to update.
    :param updates: The dictionary with updates.
    :return: A new dictionary with the updates applied.
    """
    # Make a copy of the original dictionary to avoid modifying it in place.
    result = original.copy()

    for key, value in updates.items():
        if isinstance(value, Mapping) and key in result:
            result[key] = deep_update(result[key], value)
        else:
            result[key] = value

    return result


def drop_none_values(d: Mapping[str, Any]) -> Dict[str, Any]:
    """
    Drop None values from a dictionary.

    :param d: The dictionary.
    :return: A new dictionary with the None values removed.
    """
    return {k: v for k, v in d.items() if v is not None}


def deep_setattr(d: dict, key_path: Sequence[str], value: Any):
    for key in key_path[:-1]:
        if key not in d:
            d[key] = {}
        d = d[key]
    d[key_path[-1]] = value


def deep_getattr(d: dict, key_path: Sequence[str]) -> Any:
    for key in key_path:
        if key in d:
            d = d[key]
        else:
            return None
    return d

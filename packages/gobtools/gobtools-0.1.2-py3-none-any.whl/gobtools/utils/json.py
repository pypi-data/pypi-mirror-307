"""
A module providing a utility function for formatting dictionaries as JSON strings.

This module contains a function that formats dictionaries into a JSON-formatted
string with customizable indentation and key sorting.

Functions:
    json_format(obj: dict, indent: int = 4, *, sort_keys: bool = False) -> str
        Formats a dictionary as a JSON string with customizable indentation and sorting.
"""

import json


def json_format(obj: dict, indent: int = 4, *, sort_keys: bool = False) -> str:
    """
    Format a dictionary as a JSON string.

    Arguments:
    ---------
        obj (dict): The dictionary to be formatted as a JSON string.
        indent (int, optional): The number of spaces to use for indentation.
            Default is 4.
        sort_keys (bool, optional): Whether to sort the dictionary keys in the output.
            Default is False.

    Returns:
    -------
        str: A JSON-formatted string representing the input dictionary.

    """
    return json.dumps(obj, indent=indent, sort_keys=sort_keys)

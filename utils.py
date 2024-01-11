"""
Utility functions.
"""

import json


def stringify_data(name, data_dict, start_char="", end_char=""):
    """
    Stringifies data dicts for logging.
    i.e. for fuel cell a:
    <start_char>FUELCELL_A {'temp':87.90, ...}<end_char>

    start_char and end_char must be implemented for arduino (exowatch) as well
    """

    # Name and json string separated by space
    data_str = f"{start_char}{name} {json.dumps(data_dict)}{end_char}"
    return data_str

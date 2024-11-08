"""JSON properties reader writer.
https://en.wikipedia.org/wiki/JSON
"""

import json


def read_values(
    conf_stream: object, props: list, opts: dict  # pylint: disable=unused-argument
) -> dict:
    """Read property values from a JSON file."""
    values = {}
    conf_json = json.load(conf_stream)
    for prop in props:
        if prop in conf_json:
            values[prop] = conf_json[prop]
    return values

"""YAML properties reader writer.
https://en.wikipedia.org/wiki/YAML
"""

import yaml


def read_values(
    conf_stream: object, props: list, opts: dict  # pylint: disable=unused-argument
) -> dict:
    """Read property values from a YAML file."""
    values = {}
    conf_yaml = yaml.safe_load(conf_stream)
    if conf_yaml is not None:
        for prop in props:
            if prop in conf_yaml:
                values[prop] = conf_yaml[prop]
    return values

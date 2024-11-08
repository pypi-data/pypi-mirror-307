"""INI properties reader writer.
https://en.wikipedia.org/wiki/INI_file
"""

import configparser


def read_values(
    conf_stream: object, props: list, opts: dict
) -> dict:  # pylint: disable=unused-argument
    """Read property values from a INI file."""
    values = {}
    section = opts["section"]
    conf_ini = configparser.ConfigParser()
    conf_ini.read_file(conf_stream)
    for prop in props:
        if prop in conf_ini[section]:
            values[prop] = conf_ini[section][prop]
    return values

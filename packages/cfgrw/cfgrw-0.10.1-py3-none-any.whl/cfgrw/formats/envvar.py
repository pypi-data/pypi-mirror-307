"""Environment variables properties reader writer.
https://en.wikipedia.org/wiki/Environment_variable
"""

import os


def read_values(props: list, opts: dict) -> dict:  # pylint: disable=unused-argument
    """Read property values from environment variables."""
    values = {}
    prefix = opts["prefix"]
    for prop in props:
        env_var = prefix + prop.upper()
        if env_var in os.environ:
            values[prop] = os.environ[env_var]
    return values

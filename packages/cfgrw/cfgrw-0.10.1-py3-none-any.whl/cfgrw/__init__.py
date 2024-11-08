# pylint: disable=too-many-locals,too-few-public-methods
"""
CFG-RW
&#x3D;&#x3D;&#x3D;&#x3D;&#x3D;
... .
"""
import io
import os
from jinja2 import Environment, FileSystemLoader

from .formats.envvar import read_values as read_envvar_values
from .formats.ini import read_values as read_ini_values
from .formats.json import read_values as read_json_values
from .formats.xml import read_values as read_xml_values
from .formats.yaml import read_values as read_yaml_values

JINJA_EXT = ".j2"
CONF_FORMATS = {
    "ini": {"ext": [".ini"], "read_fn": read_ini_values},
    "json": {"ext": [".json"], "read_fn": read_json_values},
    "xml": {"ext": [".xml"], "read_fn": read_xml_values},
    "yaml": {"ext": [".yaml", ".yml"], "read_fn": read_yaml_values},
}


class CFGRW:
    """A class for managing the display of text from configuration file."""

    def __init__(self, conf_file=None) -> None:
        """Initialise CFGRW."""

        self.conf_file = conf_file
        self.conf_formats = CONF_FORMATS

    def read(  # pylint: disable=dangerous-default-value
        self, props: list, opts={}
    ) -> dict:
        """Read the values of a list of properties.
        Fallback to environment variables when configuration file
        is not specified.
        """

        if self.conf_file:
            if self.conf_file.endswith(JINJA_EXT):
                j2_template_dir = os.path.dirname(self.conf_file)
                j2_template_file = os.path.basename(self.conf_file)
                j2_file_loader = FileSystemLoader(j2_template_dir)
                j2_env = Environment(loader=j2_file_loader)
                template = j2_env.get_template(j2_template_file)
                conf_string = template.render({"env": dict(os.environ)})
                conf_format = self._id_conf_format(
                    self.conf_file.replace(JINJA_EXT, "")
                )
                read_fn = conf_format["read_fn"]
                values = read_fn(io.StringIO(conf_string), props, opts)
            else:
                conf_format = self._id_conf_format(self.conf_file)
                read_fn = conf_format["read_fn"]
                with open(self.conf_file, "r", encoding="utf-8") as conf_stream:
                    values = read_fn(conf_stream, props, opts)
        else:
            values = read_envvar_values(props, opts)

        return values

    def _id_conf_format(self, conf_file: str) -> str:

        for (
            conf_format,  # pylint: disable=unused-variable
            settings,
        ) in CONF_FORMATS.items():
            if conf_file.endswith(tuple(settings["ext"])):
                return settings

        return None

"""XML properties reader writer.
https://en.wikipedia.org/wiki/XML
"""

import xml.etree.ElementTree as ET


def read_values(
    conf_stream: object, props: list, opts: dict  # pylint: disable=unused-argument
) -> dict:
    """Read property values from a JSON file."""
    values = {}
    xml_tree = ET.ElementTree(ET.fromstring(conf_stream.read()))
    conf_xml = xml_tree.getroot()
    for prop in props:
        xml_elem = conf_xml.find(prop)
        if xml_elem is not None:
            values[prop] = xml_elem.text
    return values

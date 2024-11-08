<img align="right" src="https://raw.github.com/cliffano/cfg-rw/main/avatar.jpg" alt="Avatar"/>

[![Build Status](https://github.com/cliffano/cfg-rw/workflows/CI/badge.svg)](https://github.com/cliffano/cfg-rw/actions?query=workflow%3ACI)
[![Security Status](https://snyk.io/test/github/cliffano/cfg-rw/badge.svg)](https://snyk.io/test/github/cliffano/cfg-rw)
[![Dependencies Status](https://img.shields.io/librariesio/release/pypi/cfgrw)](https://libraries.io/github/cliffano/cfg-rw)
[![Published Version](https://img.shields.io/pypi/v/cfgrw.svg)](https://pypi.python.org/pypi/cfgrw)
<br/>

CFG-RW
------

CFG-RW is a Python library for reading and writing properties in configuration files.

Installation
------------

    pip3 install cfgrw

Usage
-----

### Configuration file

CFG-RW can read configuration properties from YAML, JSON, INI, and XML files.

Create a configuration file, e.g. `cfgrw.yaml`:

    ---
    handlers: "stream,file"
    datefmt: "%Y-%m-%d %H:%M:%S"
    filename: "stage/test-integration/test-yaml-conf.log"
    filemode: "w"
    format: "%(levelname)s %(message)s"
    level: "info"

Create CFGRW object with specific conf_file, and read the values of the configuration properties:

    from cfgrw import CFGRW

    cfgrw = CFGRW(conf_file='path/to/cfgrw.yaml')
    values = cfgrw.read(['handlers', 'filemode', 'level'])
    print(value['handlers']) # will print stream,file
    print(value['filemode']) # will print w
    print(value['level']) # will print info

### Environment variables

CFG-RW can also read configuration properties from environment variables with a given prefix.

For example, here are the environment variables with prefix `CFGRW_` :

    export CFGRW_HANDLERS="stream,file"
    export CFGRW_DATEFMT="%Y-%m-%d %H:%M:%S"
    export CFGRW_FILENAME="stage/test-integration/test-yaml-conf.log"
    export CFGRW_FILEMODE="w"
    export CFGRW_FORMAT="%(levelname)s %(message)s"
    export CFGRW_LEVEL="info"

Create CFGRW object without conf_file, and read the value of the configuration properties with specified prefix:

    cfgrw = CFGRW()
    values = cfgrw.read(['handlers', 'filemode', 'level'], { 'prefix': 'CFGRW_' })
    print(value['handlers']) # will print stream,file
    print(value['filemode']) # will print w
    print(value['level']) # will print info

### Configuration file with Jinja template

CFG-RW can read configuration properties with YAML, JSON, INI, and XML within a Jinja template. You just need to add a `.j2` to the configuration file name.

Create a configuration Jinja template, e.g. `cfgrw.yaml.j2`:

    ---
    handlers: "{{ env.FOOBAR_HANDLERS }}"
    datefmt: "%Y-%m-%d %H:%M:%S"
    filename: "stage/test-integration/test-yaml-conf.log"
    filemode: "{{ env.FOOBAR_FILEMODE }}"
    format: "%(levelname)s %(message)s"
    level: "{{ env.FOOBAR_LEVEL }}"

and the following environment variables:

    export FOOBAR_HANDLERS="stream,file"
    export FOOBAR_FILEMODE="w"
    export FOOBAR_LEVEL="info"

Create CFGRW object with specific conf_file, and read the values of the configuration properties:

    from cfgrw import CFGRW

    cfgrw = CFGRW(conf_file='path/to/cfgrw.yaml.j2')
    values = cfgrw.read(['handlers', 'level', 'level'])
    print(value['handlers']) # will print stream,file
    print(value['filemode']) # will print w
    print(value['level']) # will print info

Configuration
-------------

CFG-RW automatically loads the configuration file based on the extension.

| Format | Extension |
|--------|-----------|
| [INI](https://en.wikipedia.org/wiki/INI_file) | `.ini` |
| [JSON](https://www.json.org/) | `.json` |
| [XML](https://www.w3.org/XML/) | `.xml` |
| [YAML](https://yaml.org/) | `.yaml` or `.yml` |
| [Jinja](https://jinja.palletsprojects.com/en/stable/) | `.ini.j2` or `.json.j2` or `.xml.j2` or `.yaml.j2` or `.yml.j2` |

Colophon
--------

[Developer's Guide](https://cliffano.github.io/developers_guide.html#python)

Build reports:

* [Lint report](https://cliffano.github.io/cfgrw/lint/pylint/index.html)
* [Code complexity report](https://cliffano.github.io/cfgrw/complexity/wily/index.html)
* [Unit tests report](https://cliffano.github.io/cfgrw/test/pytest/index.html)
* [Test coverage report](https://cliffano.github.io/cfgrw/coverage/coverage/index.html)
* [Integration tests report](https://cliffano.github.io/cfgrw/test-integration/pytest/index.html)
* [API Documentation](https://cliffano.github.io/cfgrw/doc/sphinx/index.html)

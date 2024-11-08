"""
pyenvs dependencies module
"""
import json
import logging
from pathlib import Path
from argparse import  Namespace

import yaml

from multienv.pyenvs_deps_formatter import Formatters
from multienv.pyenvs_deps_input_std import Configuration

LOG = logging.getLogger(__name__)

def dependencies(configuration: Configuration, formatter: Formatters) -> list:
    """Builds the environment set mapping the configuration using the given formatter."""
    return formatter.build(configuration)

def _dependencies(ns: Namespace):
    """config
    """
    LOG.info("dependencies")

    extension = ns.file.split('.')[-1]
    output_dir = Path(Path.cwd(), ns.output)

    LOG.info('open configuration file %s', ns.file)
    with open(ns.file, encoding=ns.encoding) as s:

        if extension in ['yml', 'yaml']:
            content = yaml.safe_load(s)
        elif extension == 'json':
            content = json.load(s)
        else:
            raise ValueError(f'unsupported configuration format {extension}')

        configuration = Configuration.from_dict(content)

        LOG.debug('open configuration file content: %s', configuration)
        for req_formatter in configuration.formatters:
            for supported_formatter in Formatters:
                if supported_formatter.test(req_formatter):
                    supported_formatter.write(configuration, output_dir)

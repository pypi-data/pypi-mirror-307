"""
pyenvs dependencies module
"""

import logging
from pathlib import Path
from argparse import  Namespace

import yaml

from multienv.pyenvs_lint_formatter import Formatters
from multienv.pyenvs_lint_input_std import Configuration

LOG = logging.getLogger(__name__)

def lint(configuration: Configuration, formatter: Formatters) -> list:
    """Builds the environment set mapping the configuration using the given formatter."""
    return formatter.build(configuration)

def _lint(ns: Namespace):
    """config
    """
    LOG.info("lint")

    extension = ns.file.split('.')[-1]
    output_dir = Path(Path.cwd(), ns.output)

    if extension in ['yml']:
        LOG.info('open configuration file %s', ns.file)
        with open(file=ns.file, mode='r', encoding=ns.encoding) as s:
            content = yaml.safe_load(s)
            configuration = Configuration.from_dict(content)

            LOG.debug('open configuration file content: %s', configuration)
            for req_formatter in configuration.formatters:
                for supported_formatter in Formatters:
                    if supported_formatter.test(req_formatter):
                        supported_formatter.write(configuration, output_dir)


    else:
        raise ValueError(f'unsupported configuration format {extension}')

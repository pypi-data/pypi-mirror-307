"""
pyenvs command entrypoint
"""
import logging

from argparse import ArgumentParser, Namespace

from multienv.pyenvs_deps import _dependencies
from multienv.pyenvs_lint import _lint

LOG = logging.getLogger(__name__)


def _info(ns: Namespace):
    """info
    """
    LOG.info("info %s", ns)




def _create_parser() -> ArgumentParser:

    # parse argument line
    parser = ArgumentParser(description='Multi environment management.')

    subparsers = parser.add_subparsers(dest='CMD', help='available commands')

    subparsers.add_parser('info', help='get general info')

    parser_deps = subparsers.add_parser(name='dependencies',
                                        help='generates dependency management files',
                                        aliases=['deps'])
    parser_deps.add_argument('file',
                             nargs='?',
                             help="path to the configuration file",
                             default="pyenvs-deps.yml")
    parser_deps.add_argument('--encoding', '-e',
                             nargs='?',
                             help='the configuration file encoding (default to utf-8)',
                             default='utf-8')
    parser_deps.add_argument('--output', '-o',
                             nargs='?',
                             help='the dependency management file output directory',
                             default='.')

    parser_lint = subparsers.add_parser(name='lint',
                                        help='generates linter files')
    parser_lint.add_argument('file',
                             nargs='?',
                             help="path to the configuration file",
                             default="pyenvs-lint.yml")
    parser_lint.add_argument('--encoding', '-e',
                             nargs='?',
                             help='the configuration file encoding (default to utf-8)',
                             default='utf-8')
    parser_lint.add_argument('--output', '-o',
                             nargs='?',
                             help='the linter configuration file output directory',
                             default='.')

    return parser


def entrypoint():
    """The pyenvs command entrypoint."""

    commands = {
        'info': _info,
        'dependencies': _dependencies,
        'deps': _dependencies,
        'lint': _lint
    }

    ns: Namespace = _create_parser().parse_args()

    commands[ns.CMD](ns)

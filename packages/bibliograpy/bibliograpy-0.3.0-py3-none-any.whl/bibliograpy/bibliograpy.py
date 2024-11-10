"""
bibliograpy command entrypoint
"""
import logging

from argparse import ArgumentParser, Namespace

from bibliograpy.process import _process

LOG = logging.getLogger(__name__)


def _info(ns: Namespace):
    """info
    """
    LOG.info("info %s", ns)

DEFAULT_FILE = "bibliograpy.yaml"
DEFAULT_ENCODING = 'utf-8'
DEFAULT_OUTPUT_DIR = '.'
DEFAULT_OUTPUT_FILE = 'bibliography.py'


def _create_parser() -> ArgumentParser:

    # parse argument line
    parser = ArgumentParser(description='Bibliography management.')

    subparsers = parser.add_subparsers(dest='CMD', help='available commands')

    subparsers.add_parser('info', help='get general info')

    process = subparsers.add_parser('process', help='generates bibliograpy source bibliography')
    process.add_argument('file',
                         nargs='?',
                         help="path to the bibliograpy configuration file",
                         default=DEFAULT_FILE)
    process.add_argument('--encoding', '-e',
                         nargs='?',
                         help='the bibliograpy configuration file encoding (default to utf-8)',
                         default=DEFAULT_ENCODING)
    process.add_argument('--output-dir', '-O',
                         nargs='?',
                         help='the source bibliograpy file output directory',
                         default=DEFAULT_OUTPUT_DIR)
    process.add_argument('--output-file', '-o',
                         nargs='?',
                         help='the source bibliograpy output file name',
                         default=DEFAULT_OUTPUT_FILE)
    process.add_argument('--scope', '-s',
                         nargs='?',
                         help='the scope name, must be consistent with --scope-import')
    process.add_argument('--init-scope', '-S',
                         nargs='?',
                         help='the scope import line')

    return parser


def entrypoint():
    """The pyenvs command entrypoint."""

    commands = {
        'info': _info,
        'process': _process
    }

    ns: Namespace = _create_parser().parse_args()

    commands[ns.CMD](ns)

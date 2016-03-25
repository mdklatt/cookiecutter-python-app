""" Implementation of the command line interface.

"""
from __future__ import absolute_import

from argparse import ArgumentParser

from . import __version__
from .core import config
from .core import logger


__all__ = "main",


def _cmdline(argv=None):
    """ Parse command line arguments.

    """
    parser = ArgumentParser()
    parser.add_argument("-c", "--config", action="append",
            help="config file [etc/config.yml]")
    parser.add_argument("-v", "--version", action="version",
            version="{{ cookiecutter.app_name }} {:s}".format(__version__),
            help="print version and exit")
    parser.add_argument("-w", "--warn", default="WARNING",
            help="logger warning level [WARNING]")
    return parser.parse_args(argv)


def main(argv=None):
    """ Execute the application CLI.

    Arguments are taken from sys.argv by default.

    """
    args = _cmdline(argv)
    logger.start(args.warn)
    config.load(args.config)
    return 0
 

# Make the module executable.

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except:
        logger.critical("shutting down due to fatal error")
        raise  # print stack trace

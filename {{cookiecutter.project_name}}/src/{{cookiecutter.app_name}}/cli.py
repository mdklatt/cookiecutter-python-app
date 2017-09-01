""" Implementation of the command line interface.

"""
from __future__ import absolute_import

from argparse import ArgumentParser

from . import __version__
from .api import cmd1
from .api import cmd2
from .core import config
from .core import logger


__all__ = "main",


def main(argv=None):
    """ Execute the application CLI.

    Arguments are taken from sys.argv by default.

    """
    args = _args(argv)
    logger.start(args.warn)
    logger.info("starting execution")
    config.load(args.config)
    args.command(**vars(args))
    logger.info("successful completion")
    return 0
 

def _args(argv=None):
    """ Parse command line arguments.

    """
    parser = ArgumentParser()
    parser.add_argument("-c", "--config", action="append",
            help="config file [etc/config.yml]")
    parser.add_argument("-v", "--version", action="version",
            version="{{ cookiecutter.app_name }} {:s}".format(__version__),
            help="print version and exit")
    parser.add_argument("-w", "--warn", default="WARN",
            help="logger warning level [WARN]")
    subparsers = parser.add_subparsers(title="commands")
    cmd1_parser = subparsers.add_parser("cmd1")
    cmd1_parser.set_defaults(command=cmd1)
    cmd2_parser = subparsers.add_parser("cmd2")
    cmd2_parser.set_defaults(command=cmd2)
    args = parser.parse_args(argv)
    if not args.config:
        # Don't specify this as an argument default or else it will always be
        # included in the list.
        args.config = ["etc/config.yml"]
    return args
 

# Make the module executable.

if __name__ == "__main__":
    try:
        status = main()
    except:
        logger.critical("shutting down due to fatal error")
        raise  # print stack trace
    else:
        raise SystemExit(status)

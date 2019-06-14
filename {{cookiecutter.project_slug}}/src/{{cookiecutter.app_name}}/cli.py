""" Implementation of the command line interface.

"""
from argparse import ArgumentParser
from inspect import getfullargspec

from . import __version__
from .api import cmd1
from .api import cmd2
from .core.config import config
from .core.logger import logger


__all__ = "main",


def main(argv=None):
    """ Execute the application CLI.

    :param argv: argument list to parse (sys.argv by default)
    """
    args = _args(argv)
    logger.start(args.warn or "DEBUG")  # can't use default from config yet
    logger.debug("starting execution")
    config.load(args.config)
    config.core.config = args.config
    if args.warn:
        config.core.logging = args.warn
    logger.stop()  # clear handlers to prevent duplicate records
    logger.start(config.core.logging)
    command = args.command
    args = vars(args)
    spec = getfullargspec(command)
    if not spec.varkw:
        # No kwargs, remove unexpected arguments.
        args = {key: args[key] for key in args if key in spec.args}
    try:
        command(**args)
    except RuntimeError as err:
        logger.critical(err)
        return 1
    logger.debug("successful completion")
    return 0
 

def _args(argv):
    """ Parse command line arguments.

    :param argv: argument list to parse
    """
    parser = ArgumentParser()
    parser.add_argument("-c", "--config", action="append",
            help="config file [etc/config.yml]")
    parser.add_argument("-v", "--version", action="version",
            version="{{ cookiecutter.app_name }} {:s}".format(__version__),
            help="print version and exit")
    parser.add_argument("-w", "--warn", default="WARN",
            help="logger warning level [WARN]")
    common = ArgumentParser(add_help=False)  # common subcommand arguments
    common.add_argument("--name", "-n", default="World", help="greeting name")
    subparsers = parser.add_subparsers(title="subcommands")
    _cmd1(subparsers, common)
    _cmd2(subparsers, common)
    args = parser.parse_args(argv)
    if not args.config:
        # Don't specify this as an argument default or else it will always be
        # included in the list.
        args.config = "etc/config.yml"
    return args
 

def _cmd1(subparsers, common):
    """ CLI adaptor for the api.cmd1 command.

    :param subparsers: subcommand parsers
    :param common: parser for common subcommand arguments
    """
    parser = subparsers.add_parser("cmd1", parents=[common])
    parser.set_defaults(command=cmd1)
    return


def _cmd2(subparsers, common):
    """ CLI adaptor for the api.cmd2 command.

    :param subparsers: subcommand parsers
    :param common: parser for common subcommand arguments
    """
    parser = subparsers.add_parser("cmd2", parents=[common])
    parser.set_defaults(command=cmd2)
    return


# Make the module executable.

if __name__ == "__main__":
    try:
        status = main()
    except:
        logger.critical("shutting down due to fatal error")
        raise  # print stack trace
    else:
        raise SystemExit(status)

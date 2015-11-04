""" Global application logging.

This module defines a global logger. Other modules should use this logger or
create a sublogger from it. No logging output will be emitted until at least
one handler is defined.

"""
from __future__ import absolute_import

from logging import getLogger
from logging import NullHandler
from logging import StreamHandler
from logging import Formatter


__all__ = "LOGFMT", "logger", "start_logger"


LOGFMT = "%(asctime)s;%(levelname)s;%(name)s;%(msg)s"


logger = getLogger(__name__.split(".")[0])
logger.addHandler(NullHandler())  # default to no output


def start_logger(level="WARN"):
    """ Enable the application root logger.

    Output is written to STDERR with a default logging level of WARN, or change
    this using the optional 'level' argument.

    This is intended to be called by main(), although different interfaces
    are free to do their own configuration, e.g. a CLI and a GUI may have
    different logging requirements.

    """
    # Removing the NullHandler first might be premature optimization, but
    # there's no reason to keep it around.
    handler = logger.handlers[0]
    assert isinstance(handler, NullHandler)
    logger.removeHandler(handler)
    handler = StreamHandler()
    handler.setFormatter(Formatter(LOGFMT))
    logger.addHandler(handler)
    logger.setLevel(level.upper())
    return

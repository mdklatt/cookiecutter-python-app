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


__all__ = "LOGFMT", "LOGGER", "logger"


LOGFMT = "%(asctime)s;%(levelname)s;%(name)s;%(msg)s"
LOGGER = getLogger(__name__.split(".")[0])
LOGGER.addHandler(NullHandler())


def logger():
    """ Basic LOGGER configuration.

    Output is written to stderr with a default logging level of WARN. Call
    LOGGER.setLevel() to change the logging level.

    This is intended to be called by main(), although different interfaces
    are free to do their own configuration, e.g. a CLI and a GUI may have
    different logging requirements.

    """
    handler = LOGGER.handlers[0]
    assert isinstance(handler, NullHandler)
    LOGGER.removeHandler(handler)
    handler = StreamHandler()
    handler.setFormatter(Formatter(LOGFMT))
    LOGGER.addHandler(handler)
    return

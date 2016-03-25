""" Global application logging.

All modules use the same global logging object. No messages will be emitted
until the logger is started.

"""
from __future__ import absolute_import

from logging import getLogger
from logging import Formatter
from logging import Logger
from logging import NullHandler
from logging import StreamHandler


__all__ = "logger",


class _Logger(Logger):
    """ Log messages to STDERR.

    """
    _LOGFMT = "%(asctime)s;%(levelname)s;%(name)s;%(msg)s"
    _METHODS = {"debug", "info", "warn", "error", "critical"}

    def __init__(self, name=None):
        """ Initialize this logger.

        The name defaults to the application name. Loggers with the same name
        refer to the same underlying object. Names are hierarchical, e.g.
        'parent.child' defines a logger that is a descendant of 'parent'.

        """
        self._logobj = getLogger(name or __name__.split(".")[0])
        self._logobj.addHandler(NullHandler())  # default to no output
        for name in self._METHODS:
            # Map logging methods to the underlying object. Method names
            # correspond to the desired priority.
            setattr(self, name, getattr(self._logobj, name))
        self.active = False
        return

    def start(self, level="WARN"):
        """ Start logging with this logger.

        Until the logger is started, no messages will be emitted. This applies
        to all loggers with the same name and any child loggers.

        Messages less than the given priority level will be ignored. The
        default level is 'WARN', which conforms to the *nix convention that a
        successful run should produce no diagnostic output. Available levels
        and their suggested meanings:

        DEBUG    - output useful for developers
        INFO     - trace normal program flow, especially external interactions
        WARN     - an abnormal condition was detected that might need attention
        ERROR    - an error was detected but execution continued
        CRITICAL - an error was detected and execution was halted

        """
        if self.active:
            return
        handler = StreamHandler()  # stderr
        handler.setFormatter(Formatter(self._LOGFMT))
        self._logobj.addHandler(handler)
        self._logobj.setLevel(level.upper())
        self.active = True
        return

    def stop(self):
        """ Stop logging with this logger.

        """
        if not self.active:
            return
        self._logobj.removeHandler(self._logobj.handlers[-1])
        self.active = False
        return

    def level(self):
        """ Return the priority level for this logger.

        """
        return self._logobj.getEffectiveLevel()


logger = _Logger()

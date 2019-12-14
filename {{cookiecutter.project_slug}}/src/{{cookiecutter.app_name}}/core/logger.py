""" Global application logging.

All modules use the same global logging object. No messages will be emitted
until the logger is started.

"""
from logging import Formatter
from logging import Logger as _Logger
from logging import NullHandler
from logging import StreamHandler


__all__ = "logger", "Logger"


class Logger(_Logger):
    """ Message logger.

    """
    LOGFMT = "%(asctime)s;%(levelname)s;%(name)s;%(message)s"

    def __init__(self, name=None):
        """ Initialize this logger.

        Loggers with the same name refer to the same underlying object. 
        Names are hierarchical, e.g. 'parent.child' defines a logger that is a 
        descendant of 'parent'.

        :param name: logger name (application name by default)
        """
        # With a NullHandler, client code may make logging calls without regard
        # to whether the logger has been started yet. The standard Logger API
        # may be used to add and remove additional handlers, but the
        # NullHandler should always be left in place. 
        super(Logger, self).__init__(name or __name__.split(".")[0])
        self.addHandler(NullHandler())  # default to no output
        return

    def start(self, level="WARN", stream=None):
        """ Start logging to a stream.

        Until the logger is started, no messages will be emitted. This applies
        to all loggers with the same name and any child loggers. 

        Multiple streams can be logged to by calling start() for each one.
        Calling start() more than once for the same stream will result in
        duplicate records to that stream.

        Messages less than the given priority level will be ignored. The
        default level conforms to the *nix convention that a successful run 
        should produce no diagnostic output. Call setLevel() to change the 
        logger's priority level after it has been stared. Available levels and 
        their suggested meanings:

            DEBUG - output useful for developers
            INFO - trace normal program flow, especially external interactions
            WARN - an abnormal condition was detected that might need attention
            ERROR - an error was detected but execution continued
            CRITICAL - an error was detected and execution was halted

        :param level: logger priority level
        :param stream: output stream (stderr by default)
        """
        self.setLevel(level.upper())
        handler = StreamHandler(stream)
        handler.setFormatter(Formatter(self.LOGFMT))
        handler.setLevel(self.level)
        self.addHandler(handler)
        return

    def stop(self):
        """ Stop logging with this logger.

        """
        for handler in self.handlers[1:]:
            # Remove everything but the NullHandler.
            self.removeHandler(handler)
        return


logger = Logger()

""" Global application logging.

All modules use the same global logging object. No messages will be emitted
until the logger is started.

"""
from email.message import EmailMessage
from email.utils import localtime
from logging import Formatter
from logging import Logger as _Logger
from logging import NullHandler
from logging import StreamHandler
from logging.handlers import BufferingHandler
from logging.handlers import SMTPHandler
from smtplib import SMTP
from smtplib import SMTP_PORT


__all__ = "EmailHandler", "Logger", "logger"


FORMAT = "%(asctime)s;%(levelname)s;%(name)s;%(message)s"


class EmailHandler(BufferingHandler, SMTPHandler):
    """ Send logger output as an email message.

    Unlike an smtplib.SMTPHandler, which sends one email for every record,
    this buffers records and sends them as a single email. This is intended
    primarily for single-shot applications that need to send out a notification
    upon failure or completion. Long-term processes need to manually flush the 
    buffer on a regular basis or otherwise as required.
    
    """
    def __init__(self, host, toaddrs, subject, credentials=None, secure=None):
        """  Initialize this object.
        
        """
        BufferingHandler.__init__(self, 1024)  # TODO: capacity class attribute
        SMTPHandler.__init__(self, host, toaddrs, subject, credentials, secure, 5.0)
        self.setFormatter(Formatter(FORMAT))
        return

    def flush(self):
        """
        Override to implement custom flushing behaviour.
        This version just zaps the buffer to empty.
        """
        self.acquire()
        try:
            self._send()
            self.buffer.clear()
        finally:
            self.release()
        return

    def _send(self):
        """ Send all buffered records in a single email message.

        """
        # Adapted from smtplib.SMTPHandler.emit()
        try:
            message = EmailMessage()
            message["From"] = self.fromaddr
            message["To"] = ",".join(self.toaddrs),
            message["Subject"] = self.subject
            message.set_content("\n".join(map(self.format, self.buffer)))
            port = self.mailport or SMTP_PORT    
            smtp = SMTP(self.mailhost, port, timeout=self.timeout)
            if self.username:
                if self.secure is not None:
                    smtp.ehlo()
                    smtp.starttls(*self.secure)
                    smtp.ehlo()
                smtp.login(self.username, self.password)
            smtp.send_message(message)
            smtp.quit()
        except Exception:
            # Eh?
            #self.handleError(record)
            raise
        return

    def __del__(self):
        self.flush()
        self.close()  # doesn't call flush?

class Logger(_Logger):
    """ Message logger.

    """
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
        self.addHandler(NullHandler())  # disable output by default
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
        handler = StreamHandler(stream)
        handler.setFormatter(Formatter(FORMAT))
        self.addHandler(handler)
        self.setLevel(level.upper())
        return

    def stop(self):
        """ Stop logging with this logger.

        """
        for handler in self.handlers[1:]:
            # Remove everything but the NullHandler.
            self.removeHandler(handler)
        return


logger = Logger()

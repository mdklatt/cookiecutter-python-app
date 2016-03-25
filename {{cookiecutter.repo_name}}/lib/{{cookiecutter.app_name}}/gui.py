""" Implementation of the graphical user interface.

"""
from __future__ import absolute_import

from .core import config
from .core import logger


__all__ = "main",


def main():
    """ Execute the application GUI.

    """
    logger.start()
    config.load(["etc/config.yml"])
    return 0
    

# Make the module executable.

if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except:
        logger.critical("shutting down due to fatal error")
        raise  # print stack trace

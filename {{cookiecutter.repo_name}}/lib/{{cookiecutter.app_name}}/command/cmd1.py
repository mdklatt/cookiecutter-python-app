""" Implement the cmd1 command.

"""
from __future__ import absolute_import

from ..core import logger


def main(**kwargs):
    """ Execute the command.
    
    """
    # Using kwargs to provide a generic interface across all commands.
    logger.debug("executing cmd1 command")
    return 0

""" Implement the cmd1 subcommand.

"""
from __future__ import absolute_import

from ..core import logger


def main(**kwargs):
    """ Execute the command.
    
    """
    # Using kwargs to provide a generic interface across all commands.
    logger.debug("executing cmd1 subcommand")
    return 0

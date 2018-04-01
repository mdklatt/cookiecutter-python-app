""" Implement the cmd1 command.

"""
from ..core import logger


def main(name="World"):
    """ Execute the command.
    
    """
    logger.debug("executing cmd1 command")
    print("Hello, {:s}!".format(name))
    return

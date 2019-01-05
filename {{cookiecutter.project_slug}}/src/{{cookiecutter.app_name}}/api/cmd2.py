""" Implement the cmd2 command.

"""
from ..core.logger import logger


def main(name="World"):
    """ Execute the command.
    
    """
    logger.debug("executing cmd2 command")
    print("Hello, {:s}!".format(name))
    return

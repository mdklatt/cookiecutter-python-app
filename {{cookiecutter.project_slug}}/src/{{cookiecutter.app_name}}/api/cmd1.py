""" Implement the cmd1 command.

"""
from ..core.logger import logger


def main(name="World"):
    """ Execute the command.
    
    :param name: name to use in greeting
    """
    logger.debug("executing cmd1 command")
    print("Hello, {:s}!".format(name))
    return

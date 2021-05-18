""" Implement the hello command.

"""
from ..core.logger import logger


def main(name="World") -> str:
    """ Execute the command.
    
    :param name: name to use in greeting
    """
    logger.debug("executing hello command")
    return f"Hello, {name}!"

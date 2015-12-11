""" Global application configuration.

This module defines a global configuration object. Other modules should use
this object to store application-wide configuration values.

"""
from __future__ import absolute_import

from yaml import load

from ._logger import logger


__all__ = "config",


class _AttrDict(dict):
    """ A dict with attribute access.

    """
    def __getattr__(self, name):
        """ Access a dict value as an attribute.

        """
        value = self[name]
        if isinstance(value, dict):
            # Allow recursive attribute access.
            value = _AttrDict(value)
        return value


class _Config(_AttrDict):
    """ Store configuration data.

    Data can be accessed as dict values or object attributes.

    """
    def __init__(self, paths=None):
        """ Initialize this object.

        """
        super(_Config, self).__init__()
        if paths:
            self.load(paths)
        return

    def load(self, paths):
        """ Load data from configuration files.

        Configuration values are read from a sequence of one or more YAML
        files. Files are read in the given order, and a duplicate value will
        overwrite the existing value.

        """
        for path in paths:
            with open(path, "r") as stream:
                logger.info("reading config data from {:s}".format(path))
                self.update(load(stream))
        return


config = _Config()

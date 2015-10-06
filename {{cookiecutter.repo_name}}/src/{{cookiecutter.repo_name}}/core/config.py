""" Global application configuration.

This module defines a global configuration object. Other modules should use
this object to store application-wide configuration values.

"""
from __future__ import absolute_import

from yaml import load

from . import LOGGER


__all__ = "CONFIG", "config"


CONFIG = {}


def config(paths):
    """ Load configuration files.

    Configuration values are read from a sequence of one or more YAML files.
    Files are read in the given order, and a duplicate value will overwrite the
    existing value. This allows for hierarchical configuration where additional
    files are free to define new values without having to provid all config
    values themselves.

    """
    for path in paths:
        with open(path, "r") as stream:
            LOGGER.info("reading config data from {:s}".format(path))
            CONFIG.update(load(stream))
    return
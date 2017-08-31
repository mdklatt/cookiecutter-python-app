""" Global application configuration.

This module defines a global configuration object. Other modules should use
this object to store application-wide configuration values.

"""
from __future__ import absolute_import

from re import compile
from yaml import load

from ._logger import logger


__all__ = "config",


class _AttrDict(dict):
    """ A dict-like object with attribute access.

    """
    def __getitem__(self, key):
        """ Access dict values by key.

        """
        value = super(_AttrDict, self).__getitem__(key)
        if isinstance(value, dict):
            # For mixed recursive assignment (e.g. `a["b"].c = value` to work
            # as expected, all dict-like values must themselves be _AttrDicts.
            # The "right way" to do this would be to convert to an _AttrDict on
            # assignment, but that requires overriding both __setitem__
            # (straightforward) and __init__ (good luck). An explicit type
            # check is used here instead of EAFP because exceptions would be
            # frequent for hierarchical data with lots of nested dicts.
            self[key] = value = _AttrDict(value)
        return value

    def __getattr__(self, key):
        """ Get dict values as attributes.

        """
        return self[key]

    def __setattr__(self, key, value):
        """ Set dict values as attributes.

        """
        self[key] = value
        return


class _Config(_AttrDict):
    """ Store configuration data.

    Data can be accessed as dict values or object attributes.

    """
    def __init__(self, paths=None, params=None):
        """ Initialize this object.

        """
        super(_Config, self).__init__()
        if paths:
            self.load(paths, params)
        return

    def load(self, paths, params=None):
        """ Load data from configuration files.

        Configuration values are read from a sequence of one or more YAML
        files. Files are read in the given order, and a duplicate value will
        overwrite the existing value.

        The optional 'params' argument is a dict-like object to use for
        parameter substitution in the config files. Any text matching "%key;"
        will be replaced with the value for 'key' in params.

        """
        def replace(match):
            """ Callback for re.sub to do parameter replacement. """
            # This allows for multi-pattern substitution in a single pass.
            return params[match.group(0)]

        params = {r"%{:s};".format(key): val for (key, val) in
                  params.items()} if params else {}
        regex = compile("|".join(params) or r"^(?!)")
        for path in paths:
            with open(path, "r") as stream:
                # Global text substitution is used for parameter replacement.
                # Two drawbacks of this are 1) the entire config file has to be
                # read into memory first; 2) it might be nice if comments were
                # excluded from replacement. A more elegant (but complex)
                # approach would be to use PyYAML's various hooks to do the
                # substitution as the file is parsed.
                logger.info("reading config data from '{:s}'".format(path))
                yaml = regex.sub(replace, stream.read())
            try:
                self.update(load(yaml))
            except TypeError:  # load() returned None
                logger.warn("config file '{:s}' is empty".format(path))
        return


config = _Config()

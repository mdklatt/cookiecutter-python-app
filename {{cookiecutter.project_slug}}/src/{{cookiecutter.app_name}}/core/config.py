""" Global application configuration.

This module defines a global configuration object. Other modules should use
this object to store application-wide configuration values.

"""
from re import compile
from yaml import load

from .logger import logger


__all__ = "config", "YamlConfig"


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


class YamlConfig(_AttrDict):
    """ Store YAML configuration data.

    Data can be accessed as dict values or object attributes.

    """
    def __init__(self, path=None, root=None, params=None):
        """ Initialize this object.

        """
        super(YamlConfig, self).__init__()
        if path:
            self.load(path, root, params)
        return

    def load(self, path, root=None, params=None):
        """ Load data from YAML configuration files.

        Configuration values are read from a sequence of one or more YAML
        files. Files are read in the given order, and a duplicate value will
        overwrite the existing value. If 'root' is specified the config data
        will be loaded under that attribute instead of the dict root.

        The optional 'params' argument is a dict-like object to use for 
        parameter substitution in the config files. Any text matching "%key;" 
        will be replaced with the value for 'key' in params.

        """
        def replace(match):
            """ Callback for re.sub to do macro replacement. """
            # This allows for multi-pattern substitution in a single pass.
            return params[match.group(0)]

        params = {r"%{:s};".format(key): val for (key, val) in
                  params.items()} if params else {}
        regex = compile("|".join(params) or r"^(?!)")
        for path in [path] if isinstance(path, str) else path:
            with open(path, "r") as stream:
                # Global text substitution is used for macro replacement. Two
                # drawbacks of this are 1) the entire config file has to be
                # read into memory first; 2) it might be nice if comments were
                # excluded from replacement. A more elegant (but complex)
                # approach would be to use PyYAML's various hooks to do the
                # substitution as the file is parsed.
                logger.info("reading config data from '{:s}'".format(path))
                yaml = regex.sub(replace, stream.read())
            data = load(yaml)
            try:
                if root:
                    self.setdefault(root, {}).update(data)
                else:
                    self.update(data)
            except TypeError:  # data is None
                logger.warn("config file {:s} is empty".format(path))
        return


config = YamlConfig()

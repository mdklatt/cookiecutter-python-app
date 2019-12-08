""" Global application configuration.

This module defines a global configuration object. Other modules should use
this object to store application-wide configuration values.

"""
from re import compile
from yaml import safe_load

from .logger import logger


__all__ = "config", "YamlConfig"


class _AttrDict(dict):
    """ A dict-like object with attribute access.

    """
    def __getitem__(self, key):
        """ Access dict values by key.

        :param key: key to retrieve
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

        :param key: key to retrieve
        """
        return self[key]

    def __setattr__(self, key, value):
        """ Set dict values as attributes.

        :param key: key to set
        :param value: new value for key
        """
        self[key] = value
        return


class YamlConfig(_AttrDict):
    """ Store YAML configuration data.

    Data can be accessed as dict values or object attributes.

    """
    def __init__(self, path=None, root=None, macros=None):
        """ Initialize this object.

        :param path: config file path to load
        :param root: place config values at this root
        :param macros: macro substitutions
        """
        super(YamlConfig, self).__init__()
        if path:
            self.load(path, root, macros)
        return

    def load(self, path, root=None, macros=None):
        """ Load data from YAML configuration files.

        Configuration values are read from a sequence of one or more YAML
        files. Files are read in the given order, and a duplicate value will
        overwrite the existing value. If 'root' is specified the config data
        will be loaded under that attribute instead of the dict root.

        The optional 'macros' argument is a dict-like object to use for macro
        substitution in the config files. Any text matching "%key;" will be
        replaced with the value for 'key' in 'macros'.

        :param path: config file path to load
        :param root: place config values at this root
        :param macros: macro substitutions
        """
        def replace(match):
            """ Callback for re.sub to do macro replacement. """
            # This allows for multi-pattern substitution in a single pass.
            return macros[match.group(0)]

        macros = {r"%{:s};".format(key): val for (key, val) in
                  macros.items()} if macros else {}
        regex = compile("|".join(macros) or r"^(?!)")
        for path in [path] if isinstance(path, str) else path:
            # TODO: Use f-strings with Python 3.6+.
            # TODO: Don't need open(str(path)) with Python 3.6+
            with open(str(path), "r") as stream:
                # Global text substitution is used for macro replacement. Two
                # drawbacks of this are 1) the entire config file has to be
                # read into memory first; 2) it might be nice if comments were
                # excluded from replacement. A more elegant (but complex)
                # approach would be to use PyYAML's various hooks to do the
                # substitution as the file is parsed.
                logger.info("reading config data from '{!s}'".format(path))
                yaml = regex.sub(replace, stream.read())
            data = safe_load(yaml)
            try:
                if root:
                    self.setdefault(root, {}).update(data)
                else:
                    self.update(data)
            except TypeError:  # data is None
                logger.warning("config file {!s} is empty".format(path))
        return


config = YamlConfig()

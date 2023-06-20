""" Global application configuration.

This module defines a global configuration object. Other modules should use
this object to store application-wide configuration values.

"""
from pathlib import Path
from string import Template
import re
try:
    import tomllib  # Python 3.11+
except ModuleNotFoundError:
    import tomli as tomllib

from .logger import logger


__all__ = "config", "TomlConfig"


class _AttrDict(dict):
    """ A dict-like object with attribute access.

    """
    def __getitem__(self, key: str):
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

    def __getattr__(self, key: str) -> object:
        """ Get dict values as attributes.

        :param key: key to retrieve
        """
        return self[key]

    def __setattr__(self, key: str, value: object):
        """ Set dict values as attributes.

        :param key: key to set
        :param value: new value for key
        """
        self[key] = value
        return


class TomlConfig(_AttrDict):
    """ Store data from TOML configuration files.

    """
    def __init__(self, paths=None, root=None, params=None):
        """ Initialize this object.

        :param paths: one or more config file paths to load
        :param root: place config values at this root
        :param params: mapping of parameter substitutions
        """
        super().__init__()
        if paths:
            self.load(paths, root, params)
        return

    def load(self, paths, root=None, params=None):
        """ Load data from configuration files.

        Configuration values are read from a sequence of one or more TOML
        files. Files are read in the given order, and a duplicate value will
        overwrite the existing value. If a root is specified the config data
        will be loaded under that attribute.

        :param paths: one or more config file paths to load
        :param root: place config values at this root
        :param params: mapping of parameter substitutions
        """
        try:
            paths = [Path(paths)]
        except TypeError:
            # Assume this is a sequence of paths.
            pass
        if params is None:
            params = {}
        for path in paths:
            # Comments must be stripped prior to template substitution to avoid
            # any unintended semantics such as stray `$` symbols.
            comment = re.compile(r"\s*#.*$", re.MULTILINE)
            with open(path, "rt") as stream:
                logger.info(f"Reading config data from '{path}'")
                conf = comment.sub("", stream.read())
                toml = Template(conf).substitute(params)
                data = tomllib.loads(toml)
            if root:
                self.setdefault(root, {}).update(data)
            else:
                self.update(data)
        return


config = TomlConfig()

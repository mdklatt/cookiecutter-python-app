""" Global application configuration.

This module defines a global configuration object. Other modules should use
this object to store application-wide configuration values.

"""
from dotenv import load_dotenv
from yaml import Node
from yaml import SafeLoader
from yaml import safe_load
from os import environ
from re import compile
from string import Template

from .logger import logger


__all__ = "config", "YamlConfig"


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


class YamlConfig(_AttrDict):
    """ Store YAML configuration data.

    Parameters can be embedded in the YAML file using e.g. $param or ${param}.
    Parameter lookup is performed against the current environment and an
    optional user-specified mapping (user parameters take precedence).

    After loading, data can be accessed as dict values or object attributes.

    """
    def __init__(self, path=None, root=None, params=None):
        """ Initialize this object.

        :param path: config file path to load
        :param root: place config values at this root
        :param params: macro substitutions
        """
        super(YamlConfig, self).__init__()
        if path:
            self.load(path, root, params)
        return

    def load(self, path, root=None, params=None):
        """ Load data from YAML configuration files.

        Configuration values are read from a sequence of one or more YAML
        files. Files are read in the given order, and a duplicate value will
        overwrite the existing value. If a root is specified the config data
        will be loaded under that attribute.

        :param path: config file path to load
        :param root: place config values at this root
        :param params: mapping of parameter substitutions
        """
        load_dotenv()
        tag = _ParameterTag(params)
        tag.add(SafeLoader)
        for path in [path] if isinstance(path, str) else path:
            # TODO: Use f-strings with Python 3.6+.
            # TODO: Don't need open(str(path)) with Python 3.6+
            with open(str(path), "r") as stream:
                logger.info("reading config data from '{!s}'".format(path))
                data = safe_load(stream)
            try:
                if root:
                    self.setdefault(root, {}).update(data)
                else:
                    self.update(data)
            except TypeError:  # data is None
                logger.warning("config file {!s} is empty".format(path))
        return


class _ParameterTag(object):
    """ YAML tag for performing parameter substitution on a scalar node.

    Enable this tag by calling add_constructor() for the SafeLoader class.

    """
    NAME = "param"

    def __init__(self, params=None):
        """ Initialize this object.

        :param params: key-value replacement mapping
        """
        self._params = environ.copy()
        try:
            self._params.update(params)
        except TypeError:
            pass  # params is None
        return

    def __call__(self, loader: SafeLoader, node: Node) -> str:
        """ Implement the tag constructor interface.

        :param loader: YAML loader
        :param node: YAML node to process
        :return: final value
        """
        value = loader.construct_scalar(node)
        return Template(value).substitute(self._params)

    def add(self, loader: type(SafeLoader)):
        """ Add this tag to the SafeLoader class.

        This adds a the tag constructor and an implicit resolver to the
        loader

        :param loader: loader class
        """
        loader.add_implicit_resolver(self.NAME, compile(r"(?=.*$)"), None)
        loader.add_constructor(self.NAME, self)
        return


config = YamlConfig()

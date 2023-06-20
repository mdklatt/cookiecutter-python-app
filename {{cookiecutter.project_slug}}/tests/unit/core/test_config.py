""" Test suite for the core.config module.

"""
from pathlib import Path

import pytest
from {{ cookiecutter.app_name }}.core.config import *  # tests __all__


class TomlConfigTest(object):
    """ Test suite for the YamlConfig class.

    """
    @classmethod
    @pytest.fixture
    def files(cls, tmp_path):
        """ Return configuration files for testing.

        """
        files = "conf1.toml", "conf2.toml"
        return tuple(Path("tests", "assets", item) for item in files)

    @classmethod
    @pytest.fixture
    def params(cls):
        """ Define configuration parameters.

        """
        return {"var1": "VAR1", "var2": "VAR2", "var3": "VAR3"}

    def test_item(self):
        """ Test item access.

        """
        config = TomlConfig()
        config["root"] = {}
        config["root"]["key"] = "value"
        assert config["root"]["key"] == "value"
        return

    def test_attr(self):
        """ Test attribute access.

        """
        config = TomlConfig()
        config.root = {}
        config.root.key = "value"
        assert config.root.key == "value"
        return

    @pytest.mark.parametrize("root", (None, "root"))
    def test_init(self, files, params, root):
        """ Test the __init__() method for loading a file.

        """
        merged = {"str": "$str", "var": "VAR1VAR3"}
        config = TomlConfig(files, root, params)
        if root:
            assert config == {root: merged}
        else:
            assert config == merged
        return

    @pytest.mark.parametrize("root", (None, "root"))
    def test_load(self, files, params, root):
        """ Test the load() method.

        """
        merged = {"str": "$str", "var": "VAR1VAR3"}
        config = TomlConfig()
        config.load(files, root, params)
        if root:
            assert config == {root: merged}
        else:
            assert config == merged
        return


# Make the module executable.

if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__]))

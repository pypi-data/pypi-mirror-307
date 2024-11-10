
import pytest
from pytest import MonkeyPatch

from bumgr import get_config

# Note: Other config files, located e.g. at '/etc/bumgr/config.toml'
# or in the user path (if 'XDG_CONFIG_HOME' is not defined) are hard
# to test, because it requires accessing and changing the users files.


def test_get_config_xdg_config(tmp_path, monkeypatch: MonkeyPatch):
    config_dir = tmp_path / "bumgr"
    config_dir.mkdir(exist_ok=False)
    config_file = config_dir / "config.toml"
    config_file.touch(exist_ok=False)
    with monkeypatch.context() as m:
        m.setenv("XDG_CONFIG_HOME", str(tmp_path))
        config = get_config()
        assert config == config_file


def test_get_config_param(tmp_path):
    config_file = tmp_path / "config.toml"
    with pytest.raises(FileNotFoundError):
        get_config(str(config_file))
    config_file.touch(exist_ok=False)
    config = get_config(str(config_file))
    assert config == config_file

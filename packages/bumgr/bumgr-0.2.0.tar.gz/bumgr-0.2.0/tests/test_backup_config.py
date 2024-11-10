import pytest

from bumgr.backup import Backup
from bumgr.config import ConfigError


@pytest.fixture
def working_config():
    return {"source": "test", "repository": "test_repo", "password_file": "foo"}


@pytest.fixture
def clean_env():
    mpatch = pytest.MonkeyPatch()
    with mpatch.context() as m:
        m.delenv("RESTIC_REPOSITORY", raising=False)
        m.delenv("RESTIC_PASSWORD_FILE", raising=False)
        m.delenv("RESTIC_PASSWORD_COMMAND", raising=False)
        yield


@pytest.mark.parametrize("field", ["source", "repository", "password_file"])
@pytest.mark.usefixtures("clean_env")
def test_backup_check_config_required(field, working_config):
    Backup.check_config(working_config)
    with pytest.raises(ConfigError):
        del working_config[field]
        Backup.check_config(working_config)


@pytest.mark.usefixtures("clean_env")
def test_backup_check_config_password_exclusive(working_config):
    Backup.check_config(working_config)
    with pytest.raises(ConfigError, match="mutually exclusive"):
        working_config["password_command"] = "should not be set"
        Backup.check_config(working_config)


@pytest.mark.usefixtures("clean_env")
def test_backup_check_config_password_command(working_config):
    del working_config["password_file"]
    working_config["password_command"] = "some command"
    Backup.check_config(working_config)


@pytest.mark.parametrize(
    "env",
    [
        "RESTIC_PASSWORD_COMMAND",
        "RESTIC_PASSWORD_FILE",
    ],
)
@pytest.mark.usefixtures("clean_env")
def test_backup_check_config_password_env(
    env, working_config: dict, monkeypatch: pytest.MonkeyPatch
):
    del working_config["password_file"]
    with pytest.raises(ConfigError):
        Backup.check_config(working_config)
    with monkeypatch.context() as m:
        m.setenv(env, "test")
        Backup.check_config(working_config)


@pytest.mark.usefixtures("clean_env")
def test_backup_check_config_mount(working_config):
    with pytest.raises(ConfigError, match="mount"):
        Backup.check_config(working_config, subcommand="mount")


@pytest.mark.usefixtures("clean_env")
def test_backup_check_config_repo_env(working_config, monkeypatch):
    del working_config["repository"]
    with pytest.raises(ConfigError):
        Backup.check_config(working_config)
    with monkeypatch.context() as m:
        m.setenv("RESTIC_REPOSITORY", "test")
        Backup.check_config(working_config)

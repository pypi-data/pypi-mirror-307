import sys
from os.path import expanduser
from unittest.mock import MagicMock

import pytest

from bumgr.backup import Backup


@pytest.mark.parametrize(
    "config, output",
    [
        (
            dict(repository="test", password_file="./file"),
            'RESTIC_REPOSITORY="test" RESTIC_PASSWORD_FILE="./file"',
        ),
        (
            dict(repository="test", password_command="somecommand"),
            'RESTIC_REPOSITORY="test" RESTIC_PASSWORD_COMMAND="somecommand"',
        ),
        (
            dict(
                repository="repo",
                password_file="file",
                env=dict(bar="val", foo=42),
            ),
            'RESTIC_REPOSITORY="repo" RESTIC_PASSWORD_FILE="file" bar="val" foo="42"',
        ),
        (
            dict(repository="test", password_file="~/file"),
            f'RESTIC_REPOSITORY="test" RESTIC_PASSWORD_FILE="{expanduser("~/file")}"',
        ),
        (
            dict(repository="~/local", password_file="file"),
            f'RESTIC_REPOSITORY="{expanduser("~/local")}" RESTIC_PASSWORD_FILE="file"',
        ),
    ],
)
def test_backup_env_output(config, output, monkeypatch: pytest.MonkeyPatch):
    mock_write = MagicMock()
    backup = Backup("some_source", **config)
    with monkeypatch.context() as m:
        m.setattr(sys.stdout, "write", mock_write)
        backup.cli_env()
    mock_write.assert_called_once_with(output)

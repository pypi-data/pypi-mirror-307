import json
import logging
import os
import shutil
import subprocess
import sys
from contextlib import AbstractContextManager
from os.path import expanduser, expandvars
from pathlib import Path
from tempfile import mkstemp
from typing import Any, Self

from bumgr.config import ConfigError, Configurable
from bumgr.executable import Executable

logger = logging.getLogger("bumgr.backup")


class Backup(AbstractContextManager, Executable, Configurable):
    EXECUTABLE = "restic"
    # For the case that homebrew is not in PATH when bumgr is run
    EXECUTABLE_DARWIN = "/opt/homebrew/bin/restic"

    def __init__(
        self,
        source: str,
        repository: str | None = None,
        password_file: str | None = None,
        password_command: str | None = None,
        exclude: str | list[str] | None = None,
        exclude_file: str | list[str] | None = None,
        macos_exclude_item: bool = True,
        exclude_caches: bool = True,
        hostname: str | None = None,
        use_static_hostname: bool = True,
        env: dict[str, Any] | None = None,
        pass_env_all: bool = False,
        pass_env_path: bool = True,
        mount: str | None = None,
    ):
        """

        :param source:
        :param repository:
        :param password_file:
        :param password_command:
        :param exclude:
        :param exclude_file:
        :param macos_exclude_item: Use ``mdutil`` command to determine
            exclude items for macOS backups. Enabled by default.
        :param exclude_caches: Pass the '--exclude-caches' to restic.
        :param hostname: Set a hostname explicitly.
        :param use_static_hostname: Determine the static hostname. Works
            on macOS and Linux. This hostname usually never changes
            when connecting to different networks. Ignored if
            ``hostname``is set. Enabled by default.
        :param env: Optional dictionary of additional environment
            variables. Note that these environment variable are only
            passed to restic, but are not available to expand paths.
        :param pass_env_all: Whether all environment variables that are
            set when running this programm are passed to restic.
            Defaults is ``False``.
        :param pass_env_path: Whether the 'PATH' environment is passed
            to restic. Default is ``True``. Ignored if
            :param:`pass_env_all` is ``True``.
        :param mount: Mount point
        """
        self.repository = repository
        self.source = source
        self.password_file = password_file
        self.password_command = password_command
        self.exclude = (
            exclude if isinstance(exclude, list) or not exclude else [exclude]
        )
        self.exclude_file = (
            exclude_file
            if isinstance(exclude_file, list) or not exclude_file
            else [exclude_file]
        )
        self.macos_exclude_item = macos_exclude_item and os.uname()[0] == "Darwin"
        self._macos_exclude_temp_file: str | None = None
        self._hostname = hostname
        self.use_static_hostname = use_static_hostname
        self._env = env
        self.pass_env_all = pass_env_all
        self.pass_env_path = pass_env_path
        self.mount_point = mount
        self.exclude_caches = exclude_caches

    def __enter__(self) -> Self:
        if self.macos_exclude_item:
            handle, self._macos_exclude_temp_file = mkstemp()
            logger.debug(f"Created temporary file '{self._macos_exclude_temp_file}'")
            with os.fdopen(handle) as f:
                # Retrieve backup exclude items from 'mdfind' and write them
                # in the temporary file.
                logger.debug("Writing temporary exclude items...")
                subprocess.run(
                    ["mdfind", "com_apple_backup_excludeItem = 'com.apple.backupd'"],
                    stdout=f,
                    check=True,
                )
            # Temporary file can be closed because the file is passed as a
            # filename to 'restic'
        return super().__enter__()

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
        /,
    ):
        if self.macos_exclude_item:
            if self._macos_exclude_temp_file is None:
                logger.warning(
                    "Expected a temporary file for exclude items "
                    "but variable is 'None'"
                )
            else:
                temp_file_path = Path(self._macos_exclude_temp_file)
                if not temp_file_path.exists():
                    logger.warning(
                        f"Temporary file '{self._macos_exclude_temp_file}' "
                        "does not exist anymore"
                    )
                else:
                    # Remove the file using 'unlink'
                    temp_file_path.unlink()
                    logger.debug("Removed temporary file used for exclude items")
        return super().__exit__(exc_type, exc_value, traceback)  # noqa

    @property
    def hostname(self) -> str | None:
        if self._hostname:
            return self._hostname
        if not self.use_static_hostname:
            return None
        sysname = os.uname()[0]
        if sysname == "Darwin":
            result = subprocess.run(
                ["scutil", "--get", "LocalHostName"], capture_output=True, text=True
            )
            return result.stdout.strip()
        elif sysname == "Linux" and shutil.which("hostnamectl") is not None:
            result = subprocess.run(
                ["hostnamectl", "--static"], capture_output=True, text=True
            )
            return result.stdout.strip()
        return None

    @property
    def _hostname_args(self) -> tuple[str, str] | tuple:
        hostname = self.hostname
        if hostname is None:
            return ()
        else:
            return ("--host", hostname)

    @property
    def _exclude_args(self) -> list[str]:
        args = []
        if self.exclude:
            for exclude in self.exclude:
                args.append("--exclude")
                args.append(exclude)
        if self.exclude_file:
            for exclude_file in self.exclude_file:
                args.append("--exclude-file")
                args.append(self._expand_path(exclude_file))
        if self.macos_exclude_item:
            if self._macos_exclude_temp_file is None:
                raise RuntimeError(
                    "'_macos_exclude_temp_file' is 'None' but should be set."
                )
            args.append("--exclude")
            args.append(self._macos_exclude_temp_file)
        if self.exclude_caches:
            args.append("--exclude-caches")
        return args

    @property
    def _password_args(self) -> tuple[str, str] | tuple:
        match (self.password_file, self.password_command):
            case (str(password_file), None):
                return ("--password-file", self._expand_path(password_file))
            case (None, str(password_command)):
                return ("--password-command", password_command)
            case (None, None):
                return ()
            case _:
                # There are many possibilities: Either both values are
                # set, but this should have been checked before. It is
                # also possible that neither values are of type str.
                # Eitherway, a ConfigError should be raised.
                raise ConfigError(
                    (
                        "password_file, password_command",
                        "Invalid values for 'password_file' and 'password_command'. "
                        "Only one of the attributes can be set at a time "
                        "and it has to be a valid string.",
                    )
                )

    @staticmethod
    def _expand_path(path: str) -> str:
        """Expands a given path to resolve variables like $HOME and
        user directories indicated by '~'.
        """
        return expanduser(expandvars(path))

    @property
    def _repo_args(self) -> tuple[str, str] | tuple:
        if self.repository is not None:
            return ("--repo", self._expand_path(self.repository))
        else:
            return ()

    @property
    def env(self) -> dict:
        envs: dict[str, str | None] = dict()
        if self.pass_env_all:
            envs.update(os.environ)
        elif self.pass_env_path:
            envs["PATH"] = os.getenv("PATH")
        if self._env is not None:
            envs.update(self._env)
        return envs

    def run_command(self, command: str):
        match command:
            case "init":
                self.init()
            case "backup":
                self.backup()
            case "mount":
                self.mount()
            case "env":
                self.cli_env()

    @classmethod
    def check_config(cls, config: dict, subcommand: str = "backup", **kwargs) -> None:
        errors: list[tuple[str, str]] = []
        if not config.get("source", None):
            errors.append(("source", "Field has to be set"))
        env: dict = config.get("env", {})
        if not isinstance(env, dict):
            errors.append(("env", "Expected type 'dict' but got type '{type(env)}'"))
            env = {}
        # Create a new dictionary that contains both env and envrion.
        # Used to later check if some fields are present as an
        # environment variable.
        complete_env = {}
        complete_env.update(env)
        complete_env.update(os.environ)
        # Check if 'repository' is set
        if not config.get("repository"):
            if complete_env.get("RESTIC_REPOSITORY", None) is None:
                errors.append(("repository", "Field has to be set"))
            else:
                logger.info("Using environment variable to retrieve repository")
        # Check if the 'password_*' fields are set and mutually exclusive
        password_file = config.get("password_file")
        password_command = config.get("password_command")
        if password_file and password_command:
            errors.append(
                ("password_file, password_command", "Fields are mutually exclusive")
            )
        if (not password_file) and (not password_command):
            if (
                complete_env.get("RESTIC_PASSWORD_COMMAND") is None
                and complete_env.get("RESTIC_PASSWORD_FILE") is None
            ):
                errors.append(
                    (
                        "password_file, password_command",
                        "One of the fields has to be set",
                    )
                )
            else:
                logger.info(
                    "Using environment variables to retrieve password file or command."
                )
        if subcommand == "mount":
            if not config.get("mount"):
                errors.append(
                    (
                        "mount",
                        "Field has to be set, or use command line argument instead",
                    )
                )
        if errors:
            raise ConfigError(errors)

    def cli_env(self) -> None:
        vars = {}
        if self.repository is not None:
            vars["RESTIC_REPOSITORY"] = self._expand_path(self.repository)
        if self.password_file is not None:
            vars["RESTIC_PASSWORD_FILE"] = self._expand_path(self.password_file)
        if self.password_command is not None:
            vars["RESTIC_PASSWORD_COMMAND"] = self.password_command
        if self._env is not None:
            vars.update(self._env)
        text = " ".join(f'{env}="{val}"' for env, val in vars.items())
        sys.stdout.write(text)

    def init(self) -> None:
        args = [
            self.executable,
            *self._repo_args,
            *self._password_args,
            "init",
        ]
        logger.debug(f"Running command '{' '.join(args)}'...")
        subprocess.run(args)

    def mount(self) -> None:
        if self.mount_point is None:
            raise ConfigError(
                ("mount", "Field has to be set, or use command line argument instead")
            )
        args = [
            self.executable,
            *self._repo_args,
            *self._password_args,
            "mount",
            self._expand_path(self.mount_point),
        ]
        logger.debug(f"Running command '{' '.join(args)}'...")
        try:
            subprocess.run(args, check=True)
        except KeyboardInterrupt:
            pass

    def backup(self):
        args = [
            self.executable,
            *self._repo_args,
            *self._password_args,
            "backup",
            self._expand_path(self.source),
            *self._exclude_args,
            *self._hostname_args,
            "--quiet",
            "--json",
        ]
        logger.debug(f"Running command '{' '.join(args)}'...")
        result = subprocess.run(args, capture_output=True, text=True, env=self.env)
        if result.returncode != 0:
            logger.error(f"restic failed with exit code '{result.returncode}'")
            logger.info(f"restic: {result.stderr.rstrip()}")
        for line in result.stdout.splitlines():
            try:
                message = json.loads(line)
                if message.get("message_type") == "summary":
                    files_new = message.get("files_new")
                    files_changed = message.get("files_changed")  # noqa: F841
                    dirs_new = message.get("dirs_new")  # noqa: F841
                    dirs_changed = message.get("dirs_changed")  # noqa: F841
                    data_added = message.get("data_added")  # noqa: F841
                    data_added_packed = message.get("data_added_packed")
                    total_duration = message.get("total_duration")  # noqa: F841
                    logger.info(
                        f"restic: Added {files_new} new files, "
                        f"{data_added_packed} bytes added (compressed)"
                    )
                if message.get("message_type") == "error":
                    error_message = message.get("error", {}).get("message")
                    error_during = message.get("during")
                    error_item = message.get("item")
                    logger.info(
                        f"restic: error at {error_item} (during {error_during})"
                    )
                    logger.info(f"restic: error message: {error_message}")
            except json.JSONDecodeError:
                logger.info(f"restic: {line}")

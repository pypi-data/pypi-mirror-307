import argparse
import logging
import sys
import tomllib
from contextlib import ExitStack
from pathlib import Path

from rich.console import Console
from rich.logging import RichHandler

from bumgr.backup import Backup, ConfigError
from bumgr.config import get_config, handle_config_error
from bumgr.contrib import BumgrPlugin, plugin_loader

logger = logging.getLogger("bumgr.main")


def _cli_get_all(
    config: dict,
    console: Console,
    subcommand: str,
    mount_directory: str | None = None,
) -> tuple[list[BumgrPlugin], dict[str, tuple[Backup, list[BumgrPlugin]]]]:
    has_error: bool = False
    global_plugins: list[BumgrPlugin] = []
    for plugin in config.get("plugins", []):
        try:
            global_plugins.append(plugin_loader(plugin))
        except ConfigError as error:
            has_error = True
            handle_config_error("plugins", error, console)

    backups: dict[str, tuple[Backup, list[BumgrPlugin]]] = {}
    for backup_name, backup in config.get("backups", {}).items():
        backup_plugins: list[BumgrPlugin] = []
        for plugin in backup.pop("plugins", []):
            try:
                backup_plugins.append(plugin_loader(plugin))
            except ConfigError as error:
                has_error = True
                handle_config_error(f"backups.{backup_name}.plugins", error, console)
        if mount_directory:
            backup["mount"] = mount_directory
        try:
            Backup.check_config(backup, subcommand=subcommand)
            backups[backup_name] = (Backup(**backup), backup_plugins)
        except ConfigError as error:
            has_error = True
            handle_config_error(f"backups.{backup_name}", error, console)

    if has_error:
        sys.exit(1)

    return global_plugins, backups


def cli():
    parser = argparse.ArgumentParser(
        prog="bumgr",
        description="Manage backups with restic on macOS and Linux",
    )
    parser.add_argument(
        "-c",
        "--config",
        dest="config_file",
        type=Path,
        default=None,
        help="path of the config file.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="log_level",
        action="count",
        default=0,
        help="more verbose output (-vv includes debug messages)",
    )
    parser.add_argument(
        "-q",
        "--quiet",
        dest="quiet",
        action="store_true",
        help="suppress all output",
    )
    parser.add_argument(
        "--log-file",
        dest="log_file",
        type=argparse.FileType("r"),
        default=None,
        help="optional log file. Log to stdout if no file is provided.",
    )
    parser.add_argument(
        "--no-color",
        dest="color",
        default=True,
        action="store_false",
        help="disable color output.",
    )
    subparsers = parser.add_subparsers(required=True, dest="subcommand")
    backup_parser = subparsers.add_parser("backup", help="Perform backups")
    backup_help_text = "name of the backup (as specified in the config)."
    backup_parser.add_argument(
        "backup",
        nargs="*",
        action="extend",
        default=[],
        help=f"optional {backup_help_text}",
    )
    mount_parser = subparsers.add_parser("mount", help="Mount a backup")
    mount_parser.add_argument(
        "backup",
        help=backup_help_text,
    )
    mount_parser.add_argument(
        "mount_directory",
        metavar="directory",
        nargs="?",
        help=(
            "optional mount directory. "
            "If no directory is specified, "
            "the directory is taken from the configuration file."
        ),
    )
    init_parser = subparsers.add_parser("init", help="Initialize a backup")
    init_parser.add_argument(
        "backup",
        help=backup_help_text,
    )
    env_parser = subparsers.add_parser(
        "env", help="Output config as environment variables"
    )
    env_parser.add_argument(
        "backup",
        help=backup_help_text,
    )
    args = parser.parse_args()
    console = Console(no_color=not args.color, quiet=args.quiet)
    log_level = (
        min(logging.ERROR, max(logging.WARN - int(args.log_level) * 10, logging.DEBUG))
        if not args.quiet
        else logging.CRITICAL
    )
    if args.log_file:
        logging.basicConfig(level=log_level, filename=args.log_file)
    else:
        logging.basicConfig(
            level=log_level, format="%(message)s", handlers=[RichHandler()]
        )

    config_path: Path = get_config(args.config_file)
    logger.debug("Using config file '{config_path}'")
    with config_path.open("rb") as config_file:
        try:
            config = tomllib.load(config_file)
        except tomllib.TOMLDecodeError as error:
            console.print(f"Error while reading {config_path}: {error}")
            sys.exit(1)

    global_plugins: list[BumgrPlugin]
    backups: dict[str, tuple[Backup, list[BumgrPlugin]]]
    global_plugins, backups = _cli_get_all(
        config, console, args.subcommand, getattr(args, "mount_directory", None)
    )

    if args.subcommand in ["init", "mount"] and args.backup not in backups.keys():
        console.print(
            f"Unknown backup '{args.backup}'. Valid backups are:",
        )
        console.print(backups.keys())
        sys.exit(2)

    valid_backups: set = {"all", *backups.keys()}
    invalid_backups: set = set(args.backup) - valid_backups
    if args.subcommand == "backup" and len(invalid_backups) != 0:
        console.print(
            f"Unknown backups {invalid_backups}. Valid backups are:",
        )
        console.print(valid_backups)
        sys.exit(2)

    if args.subcommand in ["backup", "init", "mount"]:
        with ExitStack() as exit_stack:
            for global_plugin in global_plugins:
                exit_stack.enter_context(global_plugin)
            if args.subcommand == "backup":
                for backup_name, (backup, plugins) in backups.items():
                    if len(args.backup) != 0 and backup_name not in args.backup:
                        continue
                    with ExitStack() as backup_exit_stack:
                        for plugin in plugins:
                            backup_exit_stack.enter_context(plugin)
                        backup_exit_stack.enter_context(backup)
                        backup.run_command(args.subcommand)
            else:
                backup, plugins = backups[args.backup]
                with ExitStack() as backup_exit_stack:
                    for plugin in plugins:
                        backup_exit_stack.enter_context(plugin)
                    backup_exit_stack.enter_context(backup)
                    backup.run_command(args.subcommand)
    elif args.subcommand == "env":
        backup, _ = backups[args.backup]
        backup.run_command(args.subcommand)

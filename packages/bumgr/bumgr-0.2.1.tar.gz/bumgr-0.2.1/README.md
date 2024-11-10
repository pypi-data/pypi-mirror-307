# Bumgr

`bumgr` is a Python CLI application to manage backups using [restic](https://restic.net/).
The name is short for "**B**ackup **M**ana**g**e**r**".

## Usage

Bumgr uses information stored in a configuration file located e.g. at
`~/.config/bumgr/config.toml`. See **Configuration** for more information.

### Backup

To backup using Bumgr, you can use the `bumgr backup` command. If you
only want to backup a specific backup configuration, you can specify
the name of the backup (as specified in your `config.toml`):
```shell
bumgr backup mybackup
```

### Mount

You may need to specify the mountpoint (an empty directory):
```shell
bumgr mount mybackup ~/Backup
```

Alternatively, you can specify the default mountpoint in the `config.toml`
file.

### Using `restic` itself

To use your configuration with the `restic` executable, you can use the
`bumgr env <backup>` command. It outputs a list of environment variables
like `RESTIC_REPOSITORY="somerepo" RESTIC_PASSWORD_FILE="some/file"`.
You can then pass these environment variables to restic:
```shell
eval $(bumgr env backupname) restic snapshots
```

## Configuration

The configuration is written in TOML and has two sections: A global section
used for defining global plugins, and a backup section that configures the
individual backups.

An example configuration could look something like this:

```toml
[backups.example_sftp]
repository = "sftp:my-backup-server.example.org:/restic"
source = "$HOME"  # backup the entire home directory
exclude_file = ["$HOME/.backup-excludes.txt", "$HOME/.gitignore_global"]
# Use macOS Keychain to retrieve password (see 'man 1 security', macOS only)
password_command = "security find-generic-password -a restic -s 'Restic Backup' -g -w"
# also possible:
# password_file = ".config/bumgr/password-file.txt"
[[backups.example_sftp]]
# Make sure Tailscale is connected before starting the backup
module = "bumgr.contrib.tailscale.Tailscale"
args.connected = true

[backups.s3example]
repository = "s3:my-s3-server.example.org/bucket/example/restic"
source = "/"
exclude = ["/var", "/dev"]
password_file = "/etc/bumgr/password-file-root.txt"
[backups.s3example.env]
AWS_ACCESS_KEY_ID = "mys3accesskey"
AWS_SECRET_ACCESS_KEY = "very-secret-key"
```

## License

Bumgr is licensed under the "BSD 3-Clause License".

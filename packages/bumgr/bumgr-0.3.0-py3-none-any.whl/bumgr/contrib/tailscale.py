import json
import subprocess

from bumgr.config import ConfigError
from bumgr.contrib import BumgrPlugin
from bumgr.executable import Executable


class Tailscale(BumgrPlugin, Executable):
    EXECUTABLE_LINUX = "/usr/bin/tailscale"
    EXECUTABLE_DARWIN = "/Applications/Tailscale.app/Contents/MacOS/Tailscale"

    def __init__(self, connected: bool = True, exit_node: str | None = None):
        self.connected = connected
        self.exit_node = exit_node
        self.prev_connection_status: bool = False
        self.prev_exit_node: str | None = None

    @classmethod
    def check_config(cls, config: dict, **kwargs) -> None:
        if (
            not config.get("connected", True)
            and config.get("exit_node", None) is not None
        ):
            raise ConfigError(
                (
                    "connected, exit_node",
                    "'connected' is 'False' but 'exit_node' is set.",
                )
            )

    def get_tailscale_status(self) -> dict:
        status_result = subprocess.run(
            [self.executable, "status", "--json"],
            check=True,
            capture_output=True,
            text=True,
        )
        return json.loads(status_result.stdout)

    def get_exit_node_status(self) -> str | None:
        status = self.get_tailscale_status()
        if "ExitNodeStatus" in status:
            exit_node_status = status["ExitNodeStatus"]
            if not exit_node_status.get("Online", False):
                return None
            # Get the ID of the current exit node
            exit_node_id = exit_node_status.get("ID", None)
            if exit_node_id is None:
                return None
            # Iterate over all peers and find a matching ID
            print(status)
            for peer in status.get("Peer", {}).values():
                if peer.get("ID", None) == exit_node_id:
                    return peer.get("HostName", None)
        return None

    def get_connection_status(self):
        status = self.get_tailscale_status()
        if "Self" in status:
            return status["Self"].get("Online", False)
        return False

    def up(self):
        subprocess.run([self.executable, "up"], check=True)

    def down(self):
        subprocess.run([self.executable, "down"], check=True)

    def set_connected(self, connected: bool):
        if connected:
            return self.up()
        else:
            return self.down()

    def set_exit_node(self, exit_node: str | None):
        exit_node_str = exit_node if exit_node is not None else ""
        subprocess.run(
            [self.executable, "set", f"--exit-node={exit_node_str}"], check=True
        )

    def __enter__(self):
        self.prev_connection_status = self.get_connection_status()
        self.prev_exit_node = self.get_exit_node_status()
        if bool(self.connected) != bool(self.prev_connection_status):
            self.set_connected(self.connected)
        if self.exit_node != self.prev_exit_node:
            self.set_exit_node(self.exit_node)
        return super().__enter__()

    def __exit__(self, exc_type, exc_value, traceback):
        if bool(self.connected) != bool(self.prev_connection_status):
            self.set_connected(self.prev_connection_status)
        if self.exit_node != self.prev_exit_node:
            self.set_exit_node(self.prev_exit_node)

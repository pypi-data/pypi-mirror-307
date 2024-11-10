import json
import subprocess
from types import SimpleNamespace
from unittest.mock import MagicMock, call

import pytest

from bumgr.contrib.tailscale import Tailscale


@pytest.mark.usefixtures("patch_executables")
def test_tailscale_status(monkeypatch: pytest.MonkeyPatch):
    tailscale = Tailscale(connected=True, exit_node="exit")
    mock = MagicMock()
    mock.return_value = SimpleNamespace()
    mock.return_value.stdout = "{}"
    with monkeypatch.context() as m:
        m.setattr(subprocess, "run", mock)
        tailscale.get_tailscale_status()
    mock.assert_called_once_with(
        [tailscale.executable, "status", "--json"],
        check=True,
        capture_output=True,
        text=True,
    )


@pytest.mark.parametrize(
    "status, ret_val",
    [
        (
            {
                "ExitNodeStatus": {"Online": True, "ID": 42},
                "Peer": {"abc": {"ID": 42, "HostName": "test42"}},
            },
            "test42",
        ),
        (
            {
                "ExitNodeStatus": {"Online": True, "ID": 42},
                "Peer": {"abc": {"ID": 43, "HostName": "test43"}},
            },
            None,
        ),
        (
            {
                "ExitNodeStatus": {"Online": False, "ID": 42},
                "Peer": {"abc": {"ID": 42, "HostName": "test42"}},
            },
            None,
        ),
        (
            {
                "ExitNodeStatus": {"Online": True},
                "Peer": {"abc": {"ID": 42, "HostName": "test42"}},
            },
            None,
        ),
        (
            {
                "Peer": {"abc": {"ID": 42, "HostName": "test42"}},
            },
            None,
        ),
    ],
)
@pytest.mark.usefixtures("patch_executables")
def test_tailscale_exit_node_status(
    status: dict, ret_val: str | None, monkeypatch: pytest.MonkeyPatch
):
    tailscale = Tailscale(connected=True, exit_node="exit")
    mock = MagicMock()
    mock.return_value = SimpleNamespace()
    mock.return_value.stdout = json.dumps(status)
    with monkeypatch.context() as m:
        m.setattr(subprocess, "run", mock)
        stat = tailscale.get_exit_node_status()
        assert stat == ret_val


@pytest.mark.parametrize(
    "status, connected",
    [
        ({"Self": {"Online": True}}, True),
        ({"Self": {"Online": False}}, False),
        ({}, False),
    ],
)
@pytest.mark.usefixtures("patch_executables")
def test_tailscale_connection_status(
    status: dict, connected: bool, monkeypatch: pytest.MonkeyPatch
):
    tailscale = Tailscale(connected=True, exit_node="exit")
    mock = MagicMock()
    mock.return_value = SimpleNamespace()
    mock.return_value.stdout = json.dumps(status)
    with monkeypatch.context() as m:
        m.setattr(subprocess, "run", mock)
        assert tailscale.get_connection_status() == connected


@pytest.mark.parametrize(
    "initial, desired",
    [(True, True), (True, False), (False, False), (False, True)],
)
@pytest.mark.usefixtures("patch_executables")
def test_tailscale_up_down(initial, desired, monkeypatch: pytest.MonkeyPatch):
    tailscale = Tailscale(connected=desired, exit_node=None)
    exe = tailscale.executable
    mock_up_down = MagicMock()
    mock_connected = MagicMock()
    mock_connected.return_value = initial
    mock_exit_node = MagicMock()
    mock_exit_node.return_value = None
    with monkeypatch.context() as m:
        m.setattr(subprocess, "run", mock_up_down)
        m.setattr(tailscale, "get_connection_status", mock_connected)
        m.setattr(tailscale, "get_exit_node_status", mock_exit_node)
        with tailscale:
            pass
        if initial == desired:
            assert mock_up_down.call_args_list == []
        else:
            calls_up_down = [
                call([exe, "up"], check=True),
                call([exe, "down"], check=True),
            ]
            if initial:
                assert mock_up_down.call_args_list == list(reversed(calls_up_down))
            else:
                assert mock_up_down.call_args_list == calls_up_down


@pytest.mark.parametrize(
    "initial, desired",
    [(None, "exitnode"), ("exitnode", None), (None, None), ("exitnode1", "exitnode2")],
)
@pytest.mark.usefixtures("patch_executables")
def test_tailscale_exit_node(initial, desired, monkeypatch: pytest.MonkeyPatch):
    tailscale = Tailscale(connected=True, exit_node=desired)
    exe = tailscale.executable
    mock_set_exit_node = MagicMock()
    mock_connected = MagicMock()
    mock_connected.return_value = True
    mock_exit_node = MagicMock()
    mock_exit_node.return_value = initial
    with monkeypatch.context() as m:
        m.setattr(subprocess, "run", mock_set_exit_node)
        m.setattr(tailscale, "get_connection_status", mock_connected)
        m.setattr(tailscale, "get_exit_node_status", mock_exit_node)
        with tailscale:
            pass
        if initial == desired:
            assert mock_set_exit_node.call_args_list == []
        else:
            assert mock_set_exit_node.call_args_list == [
                call([exe, "set", f"--exit-node={desired or ''}"], check=True),
                call([exe, "set", f"--exit-node={initial or ''}"], check=True),
            ]

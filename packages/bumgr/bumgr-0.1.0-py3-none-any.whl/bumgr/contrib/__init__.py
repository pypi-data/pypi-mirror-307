import importlib
from abc import ABCMeta
from contextlib import AbstractContextManager

from bumgr.config import ConfigError, Configurable


class BumgrPlugin(AbstractContextManager, Configurable, metaclass=ABCMeta):
    pass


def plugin_loader(plugin_spec: dict) -> BumgrPlugin:
    plugin_module_spec = plugin_spec.get("module", None)
    if plugin_module_spec is None:
        raise ConfigError(("module", "Field has to be set"))
    try:
        plugin_module_str, plugin_class_str = plugin_module_spec.rsplit(".", 1)
    except ValueError:
        raise ConfigError(("module", "Field is not a valid python class"))
    plugin_class: type[BumgrPlugin] | None
    try:
        plugin_class = getattr(
            importlib.import_module(plugin_module_str), plugin_class_str, None
        )
    except ModuleNotFoundError:
        plugin_class = None
    if plugin_class is None:
        raise ConfigError(("module", f"Class '{plugin_module_spec}' can not be found"))
    plugin_class.check_config(plugin_spec.get("args", {}))
    return plugin_class(**plugin_spec.get("args", {}))

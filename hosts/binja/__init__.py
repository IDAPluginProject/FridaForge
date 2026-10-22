"""Binary Ninja plugin entry point for FridaForge."""

import json
import os

from binaryninja import PluginCommand, log_error, log_info

PLUGIN_MENU = "FridaForge"


def _core_requirement() -> str:
    manifest = os.path.join(os.path.dirname(os.path.abspath(__file__)), "plugin.json")
    try:
        with open(manifest, encoding="utf-8") as f:
            pins = json.load(f)["dependencies"]["pip"]
    except (OSError, KeyError, TypeError, ValueError):
        return "fridaforge"
    return next((p for p in pins if p.startswith("fridaforge")), "fridaforge")


try:
    from fridaforge._version import __version__
    from fridaforge.backend import ContextKind
    from fridaforge.commands import ALL_COMMANDS
except ModuleNotFoundError as exc:
    if (exc.name or "").split(".")[0] != "fridaforge":
        raise
    _CORE_AVAILABLE = False
    log_error(
        f"[FridaForge] Core package is missing ({exc.name}). Reinstall FridaForge "
        f"from the Extension Manager, or run `pip install {_core_requirement()}` "
        "in Binary Ninja's Python environment."
    )
else:
    _CORE_AVAILABLE = True
    from .backend_binja import BinjaBackend

try:
    from binaryninjaui import UIAction, UIActionHandler
    _UI_AVAILABLE = True
except Exception:
    _UI_AVAILABLE = False


def _menu_path(command) -> str:
    if command.category:
        return f"{PLUGIN_MENU}\\{command.category}\\{command.description}"
    return f"{PLUGIN_MENU}\\{command.description}"


def _register_menu(command) -> None:
    path = _menu_path(command)
    if command.context == ContextKind.FUNCTION:
        PluginCommand.register_for_function(
            path, command.description,
            lambda bv, func, c=command: c.run(
                BinjaBackend(bv, addr=func.start, func=func)
            ),
        )
    elif command.context == ContextKind.ADDRESS:
        PluginCommand.register_for_address(
            path, command.description,
            lambda bv, addr, c=command: c.run(BinjaBackend(bv, addr=addr)),
        )
    else:
        PluginCommand.register(
            path, command.description,
            lambda bv, c=command: c.run(BinjaBackend(bv)),
        )


def _register_hotkey(command) -> None:
    if not command.hotkey or not _UI_AVAILABLE:
        return
    action_name = f"{PLUGIN_MENU}\\{command.description}"

    def _run(ctx, c=command):
        bv = getattr(ctx, "binaryView", None)
        if bv is None:
            return
        addr = getattr(ctx, "address", None)
        func = getattr(ctx, "function", None)
        c.run(BinjaBackend(bv, addr=addr, func=func))

    UIAction.registerAction(action_name, command.hotkey)
    UIActionHandler.globalActions().bindAction(action_name, UIAction(_run))


if _CORE_AVAILABLE:
    for _command in ALL_COMMANDS:
        _register_menu(_command)
        _register_hotkey(_command)

    log_info(f"[FridaForge] v{__version__} loaded.")

"""Binary Ninja plugin entry point for FridaForge."""

from binaryninja import PluginCommand, log_info

from fridaforge._version import __version__
from fridaforge.backend import ContextKind
from fridaforge.backend_binja import BinjaBackend
from fridaforge.commands import ALL_COMMANDS

PLUGIN_MENU = "FridaForge"

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
    # NOTE: confirm UIActionContext attribute names against the installed
    # Binary Ninja version during manual verification (Step 5).
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


for _command in ALL_COMMANDS:
    _register_menu(_command)
    _register_hotkey(_command)

log_info(f"[FridaForge] v{__version__} loaded.")

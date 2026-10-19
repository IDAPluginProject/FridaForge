"""IDA Pro plugin entry point for FridaForge."""

import os
import sys

import idaapi

# Ensure the parent of this plugin folder is on sys.path so that
# ``import fridaforge`` resolves (this file lives inside fridaforge/).
_plugin_dir = os.path.dirname(os.path.abspath(__file__))
_parent = os.path.dirname(_plugin_dir)
if _parent not in sys.path:
    sys.path.insert(0, _parent)

from fridaforge.backend_ida import IdaBackend
from fridaforge.commands import ALL_COMMANDS

TOP_MENU = "FridaForge"


class _CommandHandler(idaapi.action_handler_t):
    def __init__(self, command):
        super().__init__()
        self.command = command

    @property
    def action_name(self) -> str:
        return f"fridaforge:{type(self.command).__name__}"

    def activate(self, ctx):
        self.command.run(IdaBackend())
        return 1

    def update(self, ctx):
        path = TOP_MENU + "/"
        if self.command.category:
            path += self.command.category + "/"
        idaapi.attach_action_to_popup(ctx.widget, None, self.action_name, path)
        return idaapi.AST_ENABLE_FOR_WIDGET


class FridaForgePlugin(idaapi.plugin_t):
    flags = idaapi.PLUGIN_KEEP
    comment = "Generate Frida scripts from IDA Pro"
    help = "Right-click in Disassembly/Pseudocode to generate Frida snippets."
    wanted_name = "FridaForge"
    wanted_hotkey = ""

    def init(self):
        self._handlers = []
        for command in ALL_COMMANDS:
            handler = _CommandHandler(command)
            self._handlers.append(handler)
            idaapi.register_action(
                idaapi.action_desc_t(
                    handler.action_name,
                    command.description,
                    handler,
                    command.hotkey,
                )
            )
        return idaapi.PLUGIN_KEEP

    def run(self, arg):
        idaapi.msg("[FridaForge] Use right-click menus or hotkeys.\n")

    def term(self):
        for handler in self._handlers:
            idaapi.unregister_action(handler.action_name)
        self._handlers = []


def PLUGIN_ENTRY():
    return FridaForgePlugin()

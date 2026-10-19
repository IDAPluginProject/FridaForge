"""Command: generate a Frida function hook."""

from fridaforge.backend import Backend, ContextKind
from fridaforge.commands.base import Command
from fridaforge.core import FunctionHookGenerator


class FunctionHookCommand(Command):
    id = "hook_function"
    description = "Generate function hook"
    category = "Hooks"
    hotkey = "Shift+F"
    context = ContextKind.FUNCTION

    def run(self, backend: Backend) -> None:
        func = backend.get_current_function()
        if func is None:
            backend.log_warn("No function at the current location.")
            return

        module_name = backend.get_module_name()
        relative_address = backend.get_relative_address(func.start)
        snippet = FunctionHookGenerator().generate(
            module_name, relative_address, func.name
        )
        self._deliver(backend, snippet)

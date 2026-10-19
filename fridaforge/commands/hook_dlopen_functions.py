"""Command: generate Frida dlopen-family hooks."""

from fridaforge.backend import Backend, ContextKind
from fridaforge.commands.base import Command
from fridaforge.core import DlopenHookGenerator


class DlopenHooksCommand(Command):
    id = "hook_dlopen_functions"
    description = "Generate dlopen hooks (Basic for Android native libs)"
    category = "Hooks"
    hotkey = "Shift+D"
    context = ContextKind.GLOBAL

    def run(self, backend: Backend) -> None:
        module_name = backend.get_module_name()
        if not module_name:
            backend.log_warn("Could not determine the module name.")
            return

        snippet = DlopenHookGenerator().generate(module_name)
        self._deliver(backend, snippet)

"""Command: generate a Frida section protection modification."""

from fridaforge.backend import Backend, ContextKind
from fridaforge.commands.base import Command
from fridaforge.core import ModifySectionProtectionGenerator


class ModifySectionProtectionCommand(Command):
    id = "modify_section_protection"
    description = "Modify current section permissions"
    category = "Memory"
    hotkey = "Shift+M"
    context = ContextKind.ADDRESS

    def run(self, backend: Backend) -> None:
        addr = backend.get_current_address()
        if addr is None:
            backend.log_warn("Could not determine the current address.")
            return

        section_name = backend.get_section_name_at(addr)
        if not section_name:
            backend.log_warn(
                f"Could not determine the containing section for {hex(addr)}."
            )
            return

        if not section_name.startswith("."):
            backend.log_warn(
                f"Address is not in a standard section. "
                f"(Section name: {section_name})"
            )
            return

        module_name = backend.get_module_name()
        snippet = ModifySectionProtectionGenerator().generate(
            module_name, section_name
        )
        self._deliver(backend, snippet)

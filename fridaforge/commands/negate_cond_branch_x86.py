"""Command: negate an x86 conditional branch."""

from fridaforge.backend import Backend, ContextKind
from fridaforge.commands.base import Command
from fridaforge.core import NegateX86CondBranchGenerator

X86_COND_BRANCHES = {
    "je", "jne", "jz", "jnz",
    "ja", "jnbe", "jae", "jnb", "jnc",
    "jb", "jnae", "jc", "jbe", "jna",
    "jg", "jnle", "jge", "jnl",
    "jl", "jnge", "jle", "jng",
    "jo", "jno", "js", "jns",
    "jp", "jpe", "jnp", "jpo",
}


class NegateX86CondBranchCommand(Command):
    id = "negate_cond_branch_x86"
    description = "Negate cond branch instruction (x86)"
    category = "Patching"
    hotkey = "Shift+X"
    context = ContextKind.ADDRESS

    def run(self, backend: Backend) -> None:
        addr = backend.get_current_address()
        if addr is None:
            backend.log_warn("Could not determine the current address.")
            return

        mnemonic = (backend.get_instruction_mnemonic(addr) or "").lower()
        if mnemonic not in X86_COND_BRANCHES:
            backend.log_warn(
                f"Instruction at {hex(addr)} ('{mnemonic}') "
                f"is not a recognized x86 conditional branch."
            )
            return

        module_name = backend.get_module_name()
        relative_address = backend.get_relative_address(addr)
        snippet = NegateX86CondBranchGenerator().generate(
            module_name, relative_address
        )
        self._deliver(backend, snippet)

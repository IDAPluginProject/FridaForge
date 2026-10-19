"""Command: negate an ARM64 conditional branch."""

from fridaforge.backend import Backend, ContextKind
from fridaforge.commands.base import Command
from fridaforge.core import NegateArm64CondBranchGenerator

ARM64_COND_BRANCHES = {
    "b.eq", "b.ne", "b.hs", "b.lo", "b.cs",
    "b.mi", "b.pl", "b.vs", "b.vc",
    "b.hi", "b.ls", "b.ge", "b.lt",
    "b.gt", "b.le", "tbz", "tbnz",
    "cbz", "cbnz",
}


class NegateArm64CondBranchCommand(Command):
    id = "negate_cond_branch_arm64"
    description = "Negate cond branch instruction (ARM64)"
    category = "Patching"
    hotkey = "Shift+A"
    context = ContextKind.ADDRESS

    def run(self, backend: Backend) -> None:
        addr = backend.get_current_address()
        if addr is None:
            backend.log_warn("Could not determine the current address.")
            return

        mnemonic = (backend.get_instruction_mnemonic(addr) or "").lower()
        if mnemonic not in ARM64_COND_BRANCHES:
            backend.log_warn(
                f"Instruction at {hex(addr)} ('{mnemonic}') "
                f"is not a recognized ARM64 conditional branch."
            )
            return

        module_name = backend.get_module_name()
        relative_address = backend.get_relative_address(addr)
        snippet = NegateArm64CondBranchGenerator().generate(
            module_name, relative_address
        )
        backend.copy_to_clipboard(snippet)

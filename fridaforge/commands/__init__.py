"""FridaForge command registry."""

from fridaforge.commands.base import Command
from fridaforge.commands.hook_dlopen_functions import DlopenHooksCommand
from fridaforge.commands.hook_function import FunctionHookCommand
from fridaforge.commands.modify_section_protection import (
    ModifySectionProtectionCommand,
)
from fridaforge.commands.negate_cond_branch_arm64 import (
    NegateArm64CondBranchCommand,
)
from fridaforge.commands.negate_cond_branch_x86 import (
    NegateX86CondBranchCommand,
)

ALL_COMMANDS: list[Command] = [
    FunctionHookCommand(),
    DlopenHooksCommand(),
    ModifySectionProtectionCommand(),
    NegateArm64CondBranchCommand(),
    NegateX86CondBranchCommand(),
]

__all__ = ["Command", "ALL_COMMANDS"]

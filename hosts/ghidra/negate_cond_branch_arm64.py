#@runtime PyGhidra
#@category FridaForge.Patching
#@keybinding Shift A
#@menupath Tools.FridaForge.Patching.Negate cond branch instruction (ARM64)
"""FridaForge: negate an ARM64 conditional branch (Ghidra wrapper)."""
import os
import sys

sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "_lib")
)

from backend_ghidra import GhidraBackend  # noqa: E402
from fridaforge.commands.negate_cond_branch_arm64 import (  # noqa: E402
    NegateArm64CondBranchCommand,
)

NegateArm64CondBranchCommand().run(GhidraBackend(currentProgram, currentAddress))  # noqa: F821,E402

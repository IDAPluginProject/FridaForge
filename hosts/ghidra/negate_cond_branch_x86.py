#@runtime PyGhidra
#@category FridaForge.Patching
#@keybinding Shift X
#@menupath Tools.FridaForge.Patching.Negate cond branch instruction (x86)
"""FridaForge: negate an x86 conditional branch (Ghidra wrapper)."""
import os
import sys

sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "_lib")
)

from backend_ghidra import GhidraBackend  # noqa: E402
from fridaforge.commands.negate_cond_branch_x86 import (  # noqa: E402
    NegateX86CondBranchCommand,
)

NegateX86CondBranchCommand().run(GhidraBackend(currentProgram, currentAddress))  # noqa: F821,E402

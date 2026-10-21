#@runtime PyGhidra
#@category FridaForge.Memory
#@keybinding Shift M
#@menupath Tools.FridaForge.Memory.Modify current section permissions
"""FridaForge: modify current section permissions (Ghidra wrapper)."""
import os
import sys

sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "_lib")
)

from backend_ghidra import GhidraBackend  # noqa: E402
from fridaforge.commands.modify_section_protection import (  # noqa: E402
    ModifySectionProtectionCommand,
)

ModifySectionProtectionCommand().run(GhidraBackend(currentProgram, currentAddress))  # noqa: F821,E402

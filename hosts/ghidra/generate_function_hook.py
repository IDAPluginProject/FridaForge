#@runtime PyGhidra
#@category FridaForge.Hooks
#@keybinding Shift F
#@menupath Tools.FridaForge.Hooks.Generate function hook
"""FridaForge: generate a Frida function hook (Ghidra wrapper)."""
import os
import sys

sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "_lib")
)

from backend_ghidra import GhidraBackend  # noqa: E402
from fridaforge.commands.hook_function import FunctionHookCommand  # noqa: E402

FunctionHookCommand().run(GhidraBackend(currentProgram, currentAddress))  # noqa: F821,E402

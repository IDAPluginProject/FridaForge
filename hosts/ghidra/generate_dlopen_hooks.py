#@runtime PyGhidra
#@category FridaForge.Hooks
#@keybinding Shift D
#@menupath Tools.FridaForge.Hooks.Generate dlopen hooks (Basic for Android native libs)
"""FridaForge: generate Frida dlopen-family hooks (Ghidra wrapper)."""
import os
import sys

sys.path.insert(
    0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "_lib")
)

from backend_ghidra import GhidraBackend  # noqa: E402
from fridaforge.commands.hook_dlopen_functions import DlopenHooksCommand  # noqa: E402

DlopenHooksCommand().run(GhidraBackend(currentProgram, currentAddress))  # noqa: F821,E402

"""Validate the Ghidra script wrappers against the command metadata."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from fridaforge.commands import ALL_COMMANDS  # noqa: E402

GHIDRA = ROOT / "hosts" / "ghidra"

WRAPPERS = {
    "hook_function": "generate_function_hook.py",
    "hook_dlopen_functions": "generate_dlopen_hooks.py",
    "modify_section_protection": "modify_section_protection.py",
    "negate_cond_branch_arm64": "negate_cond_branch_arm64.py",
    "negate_cond_branch_x86": "negate_cond_branch_x86.py",
}


def _command(cid):
    return next(c for c in ALL_COMMANDS if c.id == cid)


def test_every_command_has_a_wrapper_file():
    for command in ALL_COMMANDS:
        assert command.id in WRAPPERS, f"no wrapper mapped for {command.id}"
        assert (GHIDRA / WRAPPERS[command.id]).exists()


def test_wrapper_metadata_matches_command():
    for cid, fname in WRAPPERS.items():
        command = _command(cid)
        text = (GHIDRA / fname).read_text(encoding="utf-8")
        assert "@runtime PyGhidra" in text
        assert f"@category FridaForge.{command.category}" in text
        assert f"@keybinding {command.hotkey.replace('+', ' ')}" in text
        menupath = f"@menupath Tools.FridaForge.{command.category}.{command.description}"
        assert menupath in text


def test_wrapper_builds_backend_and_runs_command():
    for fname in WRAPPERS.values():
        text = (GHIDRA / fname).read_text(encoding="utf-8")
        assert "from backend_ghidra import GhidraBackend" in text
        assert "GhidraBackend(currentProgram, currentAddress)" in text

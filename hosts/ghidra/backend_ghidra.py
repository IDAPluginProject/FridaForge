"""Ghidra (PyGhidra) implementation of the FridaForge Backend.

Constructed from the GhidraScript runtime globals ``currentProgram`` (a Ghidra
``Program``) and ``currentAddress`` (a Ghidra ``Address`` or ``None``). All
Ghidra/Java access is guarded so the module imports without a live Ghidra, and
the clipboard uses Java AWT, imported lazily inside the method.
"""

import os

from fridaforge.backend import Backend, FunctionRef


class GhidraBackend(Backend):
    def __init__(self, program, current_address=None):
        self._program = program
        self._current_address = current_address

    def _to_addr(self, offset: int):
        space = self._program.getAddressFactory().getDefaultAddressSpace()
        return space.getAddress(offset)

    def get_module_name(self) -> str:
        try:
            path = self._program.getExecutablePath()
            if path:
                return os.path.basename(str(path))
        except Exception:
            pass
        try:
            return str(self._program.getName())
        except Exception:
            return ""

    def get_image_base(self) -> int:
        try:
            return int(self._program.getImageBase().getOffset())
        except Exception:
            return 0

    def get_current_address(self) -> int | None:
        if self._current_address is None:
            return None
        try:
            return int(self._current_address.getOffset())
        except Exception:
            return None

    def get_current_function(self) -> FunctionRef | None:
        if self._current_address is None:
            return None
        try:
            fm = self._program.getFunctionManager()
            func = fm.getFunctionContaining(self._current_address)
        except Exception:
            return None
        if func is None:
            return None
        start = int(func.getEntryPoint().getOffset())
        raw_name = str(func.getName() or "")
        name = self._resolve_function_name(start, raw_name)
        return FunctionRef(start, name)

    def get_section_name_at(self, addr: int) -> str | None:
        try:
            block = self._program.getMemory().getBlock(self._to_addr(addr))
        except Exception:
            return None
        if block is None:
            return None
        return str(block.getName())

    def get_instruction_mnemonic(self, addr: int) -> str | None:
        try:
            insn = self._program.getListing().getInstructionAt(
                self._to_addr(addr)
            )
        except Exception:
            return None
        if insn is None:
            return None
        mnem = insn.getMnemonicString()
        return str(mnem) if mnem else None

    def copy_to_clipboard(self, text: str) -> bool:
        if not text:
            return False
        try:
            from java.awt import Toolkit
            from java.awt.datatransfer import StringSelection

            clipboard = Toolkit.getDefaultToolkit().getSystemClipboard()
            clipboard.setContents(StringSelection(text), None)
            return True
        except Exception:
            return False

    def log_info(self, msg: str) -> None:
        print(f"[FridaForge] {msg}")

    def log_warn(self, msg: str) -> None:
        print(f"[FridaForge] {msg}")

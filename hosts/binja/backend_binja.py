"""Binary Ninja implementation of the FridaForge Backend."""

import os

from binaryninja import BinaryView, Function, log_info, log_warn
from PySide6.QtWidgets import QApplication

from fridaforge.backend import Backend, FunctionRef


class BinjaBackend(Backend):
    def __init__(self, bv: BinaryView, addr: int | None = None,
                 func: Function | None = None):
        self._bv = bv
        self._addr = addr
        self._func = func

    def get_module_name(self) -> str:
        return os.path.basename(self._bv.file.original_filename)

    def get_image_base(self) -> int:
        return self._bv.start

    def get_current_address(self) -> int | None:
        return self._addr

    def get_current_function(self) -> FunctionRef | None:
        if self._func is None:
            return None
        name = self._resolve_function_name(self._func.start, self._func.name)
        return FunctionRef(self._func.start, name)

    def get_section_name_at(self, addr: int) -> str | None:
        for name, section in self._bv.sections.items():
            if section.start <= addr < section.start + section.length:
                return name
        return None

    def get_instruction_mnemonic(self, addr: int) -> str | None:
        try:
            disasm = self._bv.get_disassembly(addr)
            if not disasm:
                return None
            return disasm.split()[0]
        except Exception:
            return None

    def copy_to_clipboard(self, text: str) -> bool:
        if not text:
            return False
        app = QApplication.instance()
        if app is None:
            return False
        clipboard = app.clipboard()
        if clipboard is None:
            return False
        clipboard.setText(text)
        return True

    def log_info(self, msg: str) -> None:
        log_info(f"[FridaForge] {msg}")

    def log_warn(self, msg: str) -> None:
        log_warn(f"[FridaForge] {msg}")

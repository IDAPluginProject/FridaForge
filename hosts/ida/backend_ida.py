"""IDA Pro implementation of the FridaForge Backend."""

import os

import idaapi
import idc
from PyQt5.QtWidgets import QApplication

from fridaforge.backend import Backend, FunctionRef


class IdaBackend(Backend):
    def get_module_name(self) -> str:
        try:
            return os.path.basename(idaapi.get_input_file_path())
        except Exception:
            return ""

    def get_image_base(self) -> int:
        try:
            return idaapi.get_imagebase()
        except Exception:
            return 0

    def get_current_address(self) -> int | None:
        ea = idaapi.get_screen_ea()
        if ea == idaapi.BADADDR:
            return None
        return ea

    def get_current_function(self) -> FunctionRef | None:
        ea = idaapi.get_screen_ea()
        if ea == idaapi.BADADDR:
            return None
        func = idaapi.get_func(ea)
        if not func:
            return None
        raw_name = idaapi.get_func_name(func.start_ea) or ""
        name = self._resolve_function_name(func.start_ea, raw_name)
        return FunctionRef(func.start_ea, name)

    def get_section_name_at(self, addr: int) -> str | None:
        seg = idaapi.getseg(addr)
        if not seg:
            return None
        return idaapi.get_segm_name(seg)

    def get_instruction_mnemonic(self, addr: int) -> str | None:
        mnemonic = idc.print_insn_mnem(addr)
        return mnemonic or None

    def copy_to_clipboard(self, text: str) -> bool:
        if not text:
            return False
        app = QApplication.instance() or QApplication([])
        clipboard = app.clipboard()
        if clipboard is None:
            return False
        clipboard.setText(text)
        return True

    def log_info(self, msg: str) -> None:
        print(f"[FridaForge] {msg}")

    def log_warn(self, msg: str) -> None:
        print(f"[FridaForge] {msg}")

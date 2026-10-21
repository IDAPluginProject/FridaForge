"""Unit tests for GhidraBackend using duck-typed fakes (no live Ghidra)."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "hosts" / "ghidra"))

from backend_ghidra import GhidraBackend  # noqa: E402


class _Addr:
    def __init__(self, offset):
        self._offset = offset

    def getOffset(self):
        return self._offset


class _Space:
    def getAddress(self, offset):
        return _Addr(offset)


class _AddrFactory:
    def getDefaultAddressSpace(self):
        return _Space()


class _Func:
    def __init__(self, entry, name):
        self._entry = _Addr(entry)
        self._name = name

    def getEntryPoint(self):
        return self._entry

    def getName(self):
        return self._name


class _FuncMgr:
    def __init__(self, func):
        self._func = func

    def getFunctionContaining(self, addr):
        return self._func


class _Block:
    def __init__(self, name):
        self._name = name

    def getName(self):
        return self._name


class _Memory:
    def __init__(self, block):
        self._block = block

    def getBlock(self, addr):
        return self._block


class _Insn:
    def __init__(self, mnem):
        self._mnem = mnem

    def getMnemonicString(self):
        return self._mnem


class _Listing:
    def __init__(self, insn):
        self._insn = insn

    def getInstructionAt(self, addr):
        return self._insn


class _Program:
    def __init__(self, *, exec_path="", name="", image_base=0,
                 func=None, block=None, insn=None):
        self._exec = exec_path
        self._name = name
        self._image_base = image_base
        self._fm = _FuncMgr(func)
        self._mem = _Memory(block)
        self._listing = _Listing(insn)

    def getExecutablePath(self):
        return self._exec

    def getName(self):
        return self._name

    def getImageBase(self):
        return _Addr(self._image_base)

    def getFunctionManager(self):
        return self._fm

    def getMemory(self):
        return self._mem

    def getListing(self):
        return self._listing

    def getAddressFactory(self):
        return _AddrFactory()


def test_module_name_uses_executable_basename():
    be = GhidraBackend(_Program(exec_path="/tmp/CrackMeEasy.exe"))
    assert be.get_module_name() == "CrackMeEasy.exe"


def test_module_name_falls_back_to_program_name():
    be = GhidraBackend(_Program(exec_path="", name="CrackMeEasy.exe"))
    assert be.get_module_name() == "CrackMeEasy.exe"


def test_image_base():
    be = GhidraBackend(_Program(image_base=0x140000000))
    assert be.get_image_base() == 0x140000000


def test_current_address_none_when_missing():
    be = GhidraBackend(_Program(), current_address=None)
    assert be.get_current_address() is None


def test_current_address_offset():
    be = GhidraBackend(_Program(), current_address=_Addr(0x1234))
    assert be.get_current_address() == 0x1234


def test_current_function_named():
    prog = _Program(func=_Func(0x1000, "main"))
    be = GhidraBackend(prog, current_address=_Addr(0x1010))
    ref = be.get_current_function()
    assert ref.start == 0x1000
    assert ref.name == "main"


def test_current_function_fallback_name_when_empty():
    prog = _Program(image_base=0x1000, func=_Func(0x1200, ""))
    be = GhidraBackend(prog, current_address=_Addr(0x1200))
    ref = be.get_current_function()
    assert ref.name == "sub_200"


def test_current_function_none_without_address():
    be = GhidraBackend(_Program(func=_Func(0x1000, "main")))
    assert be.get_current_function() is None


def test_section_name_at():
    be = GhidraBackend(_Program(block=_Block(".text")))
    assert be.get_section_name_at(0x1500) == ".text"


def test_section_name_at_none():
    be = GhidraBackend(_Program(block=None))
    assert be.get_section_name_at(0x1500) is None


def test_instruction_mnemonic():
    be = GhidraBackend(_Program(insn=_Insn("je")))
    assert be.get_instruction_mnemonic(0x1500) == "je"


def test_instruction_mnemonic_none():
    be = GhidraBackend(_Program(insn=None))
    assert be.get_instruction_mnemonic(0x1500) is None


def test_copy_empty_returns_false():
    be = GhidraBackend(_Program())
    assert be.copy_to_clipboard("") is False

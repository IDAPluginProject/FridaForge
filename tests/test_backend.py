from fridaforge.backend import ContextKind, FunctionRef
from tests.fakes import FakeBackend


def test_get_relative_address_subtracts_image_base():
    be = FakeBackend(image_base=0x1000)
    assert be.get_relative_address(0x1234) == hex(0x1234 - 0x1000)


def test_resolve_function_name_uses_raw_when_present():
    be = FakeBackend(image_base=0x1000)
    assert be._resolve_function_name(0x1234, "my_func") == "my_func"


def test_resolve_function_name_falls_back_to_sub():
    be = FakeBackend(image_base=0x1000)
    # relative address is 0x234 -> fallback "sub_234"
    assert be._resolve_function_name(0x1234, "") == "sub_234"


def test_context_kind_members():
    assert {k.name for k in ContextKind} == {"GLOBAL", "ADDRESS", "FUNCTION"}


def test_function_ref_fields():
    ref = FunctionRef(start=0x10, name="f")
    assert ref.start == 0x10 and ref.name == "f"

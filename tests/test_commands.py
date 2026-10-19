from fridaforge.backend import ContextKind, FunctionRef
from fridaforge.commands.hook_function import FunctionHookCommand
from tests.fakes import FakeBackend


def test_function_hook_copies_filled_snippet():
    be = FakeBackend(
        module_name="libfoo.so",
        image_base=0x1000,
        current_function=FunctionRef(start=0x1234, name="my_func"),
    )
    FunctionHookCommand().run(be)
    assert be.clipboard is not None
    assert "libfoo.so" in be.clipboard
    assert "my_func" in be.clipboard
    assert hex(0x1234 - 0x1000) in be.clipboard


def test_function_hook_without_function_warns_and_skips():
    be = FakeBackend(current_function=None)
    FunctionHookCommand().run(be)
    assert be.clipboard is None
    assert be.warnings


def test_function_hook_metadata():
    cmd = FunctionHookCommand()
    assert cmd.context == ContextKind.FUNCTION
    assert cmd.description
    assert cmd.hotkey


from fridaforge.commands.hook_dlopen_functions import DlopenHooksCommand


def test_dlopen_copies_filled_snippet():
    be = FakeBackend(module_name="libfoo.so")
    DlopenHooksCommand().run(be)
    assert be.clipboard is not None
    assert "libfoo.so" in be.clipboard


def test_dlopen_without_module_warns_and_skips():
    be = FakeBackend(module_name="")
    DlopenHooksCommand().run(be)
    assert be.clipboard is None
    assert be.warnings


from fridaforge.commands.modify_section_protection import (
    ModifySectionProtectionCommand,
)


def test_section_protection_copies_for_valid_section():
    be = FakeBackend(
        module_name="libfoo.so",
        current_address=0x2000,
        section_at={0x2000: ".text"},
    )
    ModifySectionProtectionCommand().run(be)
    assert be.clipboard is not None
    assert ".text" in be.clipboard
    assert "libfoo.so" in be.clipboard


def test_section_protection_no_address_skips():
    be = FakeBackend(current_address=None)
    ModifySectionProtectionCommand().run(be)
    assert be.clipboard is None


def test_section_protection_no_section_warns():
    be = FakeBackend(current_address=0x2000, section_at={})
    ModifySectionProtectionCommand().run(be)
    assert be.clipboard is None
    assert be.warnings


def test_section_protection_non_dot_section_warns():
    be = FakeBackend(current_address=0x2000, section_at={0x2000: "extern"})
    ModifySectionProtectionCommand().run(be)
    assert be.clipboard is None
    assert be.warnings

from fridaforge.core.utils import fill_template, read_template


def test_fill_template_replaces_bracketed_tokens():
    out = fill_template("a=[X], b=[Y]", {"X": "1", "Y": 2})
    assert out == "a=1, b=2"


def test_fill_template_leaves_unknown_tokens():
    out = fill_template("keep [Z]", {"X": "1"})
    assert out == "keep [Z]"


def test_read_template_loads_hook_function():
    content = read_template("hook_function.js")
    assert "[MODULE_NAME_PLACEHOLDER]" in content


from fridaforge.core import (
    DlopenHookGenerator,
    FunctionHookGenerator,
    ModifySectionProtectionGenerator,
    NegateArm64CondBranchGenerator,
    NegateX86CondBranchGenerator,
)


def _assert_no_leftover_placeholders(text: str):
    import re
    assert not re.search(r"\[[A-Z_]+_PLACEHOLDER\]", text)


def test_function_hook_generator_fills_all():
    out = FunctionHookGenerator().generate("libfoo.so", "0x1234", "my_func")
    assert "libfoo.so" in out
    assert "0x1234" in out
    assert "my_func" in out
    _assert_no_leftover_placeholders(out)


def test_dlopen_generator_fills_module():
    out = DlopenHookGenerator().generate("libfoo.so")
    assert "libfoo.so" in out
    _assert_no_leftover_placeholders(out)


def test_section_protection_generator_fills_all():
    out = ModifySectionProtectionGenerator().generate("libfoo.so", ".text")
    assert "libfoo.so" in out
    assert ".text" in out
    _assert_no_leftover_placeholders(out)


def test_negate_arm64_generator_fills_all():
    out = NegateArm64CondBranchGenerator().generate("libfoo.so", "0xdead")
    assert "libfoo.so" in out
    assert "0xdead" in out
    _assert_no_leftover_placeholders(out)


def test_negate_x86_generator_fills_all():
    out = NegateX86CondBranchGenerator().generate("libfoo.so", "0xbeef")
    assert "libfoo.so" in out
    assert "0xbeef" in out
    _assert_no_leftover_placeholders(out)

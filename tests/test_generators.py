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

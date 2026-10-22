import importlib.util
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location(
    "check_wheel", ROOT / "build" / "check_wheel.py"
)
check_wheel = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(check_wheel)


def _make_wheel(path: Path, names: list[str]) -> Path:
    with zipfile.ZipFile(path, "w") as wheel:
        for name in names:
            wheel.writestr(name, "")
    return path


def test_expected_files_include_every_template():
    expected = check_wheel.expected_files()
    templates = sorted((ROOT / "fridaforge" / "templates").glob("*.js"))
    assert templates
    for template in templates:
        assert f"fridaforge/templates/{template.name}" in expected


def test_complete_wheel_passes(tmp_path):
    wheel = _make_wheel(tmp_path / "ok.whl", check_wheel.expected_files())
    assert check_wheel.check_wheel(wheel) == []


def test_missing_template_is_reported(tmp_path):
    names = [n for n in check_wheel.expected_files() if not n.endswith("hook_function.js")]
    wheel = _make_wheel(tmp_path / "missing.whl", names)
    assert check_wheel.check_wheel(wheel) == ["missing fridaforge/templates/hook_function.js"]


def test_host_and_test_files_are_reported(tmp_path):
    names = check_wheel.expected_files() + ["hosts/binja/__init__.py", "tests/fakes.py"]
    wheel = _make_wheel(tmp_path / "extra.whl", names)
    assert check_wheel.check_wheel(wheel) == [
        "unexpected hosts/binja/__init__.py",
        "unexpected tests/fakes.py",
    ]

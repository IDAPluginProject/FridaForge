import importlib.util
import sys
import types
from pathlib import Path

import pytest

from fridaforge.commands import ALL_COMMANDS

ROOT = Path(__file__).resolve().parent.parent
BINJA_DIR = ROOT / "hosts" / "binja"
ENTRY_NAME = "ff_binja_entry_under_test"
REPO_PLUGIN_NAME = "ff_repo_plugin_under_test"


def _fake_binaryninja() -> types.ModuleType:
    bn = types.ModuleType("binaryninja")
    bn.registered = []
    bn.errors = []
    bn.infos = []

    class PluginCommand:
        @staticmethod
        def register(name, description, action):
            bn.registered.append(name)

        register_for_function = register
        register_for_address = register

    bn.PluginCommand = PluginCommand
    bn.BinaryView = type("BinaryView", (), {})
    bn.Function = type("Function", (), {})
    bn.log_info = bn.infos.append
    bn.log_warn = bn.infos.append
    bn.log_error = bn.errors.append
    return bn


@pytest.fixture
def fake_bn(monkeypatch):
    bn = _fake_binaryninja()
    monkeypatch.setitem(sys.modules, "binaryninja", bn)
    monkeypatch.setitem(sys.modules, "binaryninjaui", None)
    qt_widgets = types.ModuleType("PySide6.QtWidgets")
    qt_widgets.QApplication = type("QApplication", (), {})
    monkeypatch.setitem(sys.modules, "PySide6", types.ModuleType("PySide6"))
    monkeypatch.setitem(sys.modules, "PySide6.QtWidgets", qt_widgets)
    yield bn
    for key in [k for k in sys.modules if k.startswith((ENTRY_NAME, REPO_PLUGIN_NAME))]:
        del sys.modules[key]


def _load_package(name: str, folder: Path):
    spec = importlib.util.spec_from_file_location(
        name,
        folder / "__init__.py",
        submodule_search_locations=[str(folder)],
    )
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _load_entry():
    return _load_package(ENTRY_NAME, BINJA_DIR)


def _hide_core(monkeypatch):
    for key in [k for k in sys.modules if k == "fridaforge" or k.startswith("fridaforge.")]:
        monkeypatch.delitem(sys.modules, key)
    monkeypatch.setitem(sys.modules, "fridaforge", None)


def test_registers_every_command_with_pip_installed_core(fake_bn):
    module = _load_entry()
    assert module._CORE_AVAILABLE is True
    assert len(fake_bn.registered) == len(ALL_COMMANDS)
    assert fake_bn.errors == []


def test_missing_core_logs_one_error_and_registers_nothing(fake_bn, monkeypatch):
    _hide_core(monkeypatch)
    module = _load_entry()
    assert module._CORE_AVAILABLE is False
    assert fake_bn.registered == []
    assert len(fake_bn.errors) == 1
    assert "pip install fridaforge==" in fake_bn.errors[0]
    assert "Extension Manager" in fake_bn.errors[0]


def test_repo_root_loads_binja_plugin(fake_bn):
    _load_package(REPO_PLUGIN_NAME, ROOT)
    entry = sys.modules[f"{REPO_PLUGIN_NAME}.hosts.binja"]
    assert entry._CORE_AVAILABLE is True
    assert len(fake_bn.registered) == len(ALL_COMMANDS)
    assert fake_bn.errors == []

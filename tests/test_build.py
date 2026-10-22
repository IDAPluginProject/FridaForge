import json
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def test_build_creates_both_archives(tmp_path):
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "build" / "build.py"),
            "--version", "9.9.9",
            "--out-dir", str(tmp_path),
        ],
        check=True,
        cwd=ROOT,
    )

    binja = tmp_path / "fridaforge-binja-9.9.9.zip"
    ida = tmp_path / "fridaforge-ida-9.9.9.zip"
    assert binja.exists()
    assert ida.exists()

    with zipfile.ZipFile(binja) as z:
        names = z.namelist()
        assert "fridaforge/__init__.py" in names
        assert "fridaforge/backend.py" in names
        assert "fridaforge/backend_binja.py" in names
        assert "fridaforge/plugin.json" in names
        assert "fridaforge/templates/hook_function.js" in names
        assert "fridaforge/commands/__init__.py" in names
        manifest = json.loads(z.read("fridaforge/plugin.json"))
        assert manifest["version"] == "9.9.9"
        entry = z.read("fridaforge/__init__.py").decode("utf-8")
        assert "from .backend_binja import BinjaBackend" in entry

    with zipfile.ZipFile(ida) as z:
        names = z.namelist()
        assert "fridaforge/ida_entry.py" in names
        assert "fridaforge/backend_ida.py" in names
        assert "fridaforge/ida-plugin.json" in names
        assert "fridaforge/templates/hook_function.js" in names
        manifest = json.loads(z.read("fridaforge/ida-plugin.json"))
        assert manifest["plugin"]["version"] == "9.9.9"


def test_build_creates_ghidra_archive(tmp_path):
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "build" / "build.py"),
            "--version", "9.9.9",
            "--out-dir", str(tmp_path),
        ],
        check=True,
        cwd=ROOT,
    )

    ghidra = tmp_path / "fridaforge-ghidra-9.9.9.zip"
    assert ghidra.exists()

    with zipfile.ZipFile(ghidra) as z:
        names = z.namelist()
        # wrappers at the archive root
        for wrapper in (
            "generate_function_hook.py",
            "generate_dlopen_hooks.py",
            "modify_section_protection.py",
            "negate_cond_branch_arm64.py",
            "negate_cond_branch_x86.py",
        ):
            assert wrapper in names
        # shared package + backend under _lib/
        assert "_lib/backend_ghidra.py" in names
        assert "_lib/fridaforge/__init__.py" in names
        assert "_lib/fridaforge/commands/__init__.py" in names
        assert "_lib/fridaforge/templates/hook_function.js" in names
        # no manifest in the script bundle
        assert not any(n.endswith("plugin.json") for n in names)
        assert not any(n.endswith("ida-plugin.json") for n in names)

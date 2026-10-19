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

    with zipfile.ZipFile(ida) as z:
        names = z.namelist()
        assert "fridaforge/ida_entry.py" in names
        assert "fridaforge/backend_ida.py" in names
        assert "fridaforge/ida-plugin.json" in names
        assert "fridaforge/templates/hook_function.js" in names
        manifest = json.loads(z.read("fridaforge/ida-plugin.json"))
        assert manifest["plugin"]["version"] == "9.9.9"

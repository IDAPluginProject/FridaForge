import json
from pathlib import Path

from fridaforge._version import __version__

ROOT = Path(__file__).resolve().parent.parent
BINJA_DIR = ROOT / "hosts" / "binja"
MANIFEST = BINJA_DIR / "plugin.json"
REQUIREMENTS = BINJA_DIR / "requirements.txt"
REQUIRED_FIELDS = (
    "pluginmetadataversion",
    "name",
    "author",
    "api",
    "license",
    "description",
    "longdescription",
    "version",
    "minimumbinaryninjaversion",
    "platforms",
)


def _manifest() -> dict:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def test_manifest_has_required_fields():
    data = _manifest()
    assert [k for k in REQUIRED_FIELDS if k not in data] == []
    assert data["pluginmetadataversion"] == 2
    build = data["minimumbinaryninjaversion"]
    assert isinstance(build, int) and not isinstance(build, bool)
    assert {"name", "text"} <= set(data["license"])


def test_manifest_shows_readme_as_long_description():
    assert _manifest()["longdescription"] == ""


def test_manifest_version_matches_core():
    assert _manifest()["version"] == __version__


def test_requirements_pin_core_exactly():
    assert REQUIREMENTS.read_text(encoding="utf-8") == f"fridaforge=={__version__}\n"


def test_manifest_leaves_dependencies_to_requirements_txt():
    assert "dependencies" not in _manifest()


def test_repo_root_is_not_a_binja_plugin():
    assert not (ROOT / "plugin.json").exists()
    assert not (ROOT / "__init__.py").exists()

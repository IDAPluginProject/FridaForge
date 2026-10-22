import json
from pathlib import Path

from fridaforge._version import __version__

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "plugin.json"
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


def test_manifest_pins_core_exactly():
    assert _manifest()["dependencies"]["pip"] == [f"fridaforge=={__version__}"]


def test_manifest_lives_only_at_repo_root():
    assert not (ROOT / "hosts" / "binja" / "plugin.json").exists()

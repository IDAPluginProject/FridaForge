import importlib.util
import json
import shutil
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
_spec = importlib.util.spec_from_file_location(
    "bump_version", ROOT / "build" / "bump_version.py"
)
bump_version = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bump_version)


@pytest.fixture
def repo_copy(tmp_path):
    for rel in (
        bump_version.VERSION_FILE,
        bump_version.BINJA_MANIFEST,
        bump_version.BINJA_REQUIREMENTS,
    ):
        (tmp_path / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / rel, tmp_path / rel)
    return tmp_path


def test_repo_versions_are_in_sync():
    versions = bump_version.read_versions()
    assert len(set(versions.values())) == 1, versions


def test_bump_rewrites_every_copy(repo_copy):
    bump_version.bump("1.2.3", root=repo_copy)

    assert bump_version.read_versions(repo_copy) == {
        "_version.py": "1.2.3",
        "plugin.json version": "1.2.3",
        "requirements.txt pin": "1.2.3",
    }
    manifest = json.loads((repo_copy / bump_version.BINJA_MANIFEST).read_text(encoding="utf-8"))
    assert manifest["name"] == "FridaForge"
    requirements = (repo_copy / bump_version.BINJA_REQUIREMENTS).read_text(encoding="utf-8")
    assert requirements == "fridaforge==1.2.3\n"


def test_bump_rejects_non_semver(repo_copy):
    with pytest.raises(ValueError):
        bump_version.bump("1.2", root=repo_copy)


def test_check_accepts_matching_tag(repo_copy):
    bump_version.bump("1.2.3", root=repo_copy)
    assert bump_version.check("v1.2.3", root=repo_copy) == []
    assert bump_version.check("1.2.3", root=repo_copy) == []


def test_check_reports_each_mismatch(repo_copy):
    bump_version.bump("1.2.3", root=repo_copy)
    problems = bump_version.check("v2.0.0", root=repo_copy)
    assert len(problems) == 3
    assert all("2.0.0" in p for p in problems)


def test_pin_requirement_keeps_other_lines():
    text = "other>=1\nfridaforge==0.0.1\n"
    assert bump_version.pin_requirement(text, "0.0.2") == "fridaforge==0.0.2\nother>=1\n"

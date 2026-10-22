"""Bump or check the FridaForge version in every file that records it."""

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VERSION_FILE = Path("fridaforge") / "_version.py"
BINJA_MANIFEST = Path("hosts") / "binja" / "plugin.json"
BINJA_REQUIREMENTS = Path("hosts") / "binja" / "requirements.txt"
CORE_REQUIREMENT = "fridaforge"

_SEMVER = re.compile(r"\d+\.\d+\.\d+")
_VERSION_LINE = re.compile(r'__version__ = "([^"]*)"')
_CORE_PIN = f"{CORE_REQUIREMENT}=="


def stamp_binja_manifest(data: dict, version: str) -> dict:
    data["version"] = version
    return data


def pin_requirement(text: str, version: str) -> str:
    others = [line for line in text.splitlines() if line and not line.startswith(_CORE_PIN)]
    return "\n".join([f"{_CORE_PIN}{version}", *others]) + "\n"


def read_versions(root: Path = ROOT) -> dict[str, str]:
    match = _VERSION_LINE.search((root / VERSION_FILE).read_text(encoding="utf-8"))
    manifest = json.loads((root / BINJA_MANIFEST).read_text(encoding="utf-8"))
    pins = [
        line.split("==", 1)[1].strip()
        for line in (root / BINJA_REQUIREMENTS).read_text(encoding="utf-8").splitlines()
        if line.startswith(_CORE_PIN)
    ]
    return {
        "_version.py": match.group(1) if match else "",
        "plugin.json version": manifest.get("version", ""),
        "requirements.txt pin": pins[0] if pins else "",
    }


def _write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def bump(version: str, root: Path = ROOT) -> None:
    if not _SEMVER.fullmatch(version):
        raise ValueError(f"version must look like X.Y.Z, got {version!r}")
    _write(root / VERSION_FILE, f'__version__ = "{version}"\n')
    manifest_path = root / BINJA_MANIFEST
    data = stamp_binja_manifest(json.loads(manifest_path.read_text(encoding="utf-8")), version)
    _write(manifest_path, json.dumps(data, indent=2) + "\n")
    requirements_path = root / BINJA_REQUIREMENTS
    _write(requirements_path, pin_requirement(requirements_path.read_text(encoding="utf-8"), version))


def check(expected: str, root: Path = ROOT) -> list[str]:
    expected = expected.removeprefix("v")
    return [
        f"{label} is {found!r}, expected {expected!r}"
        for label, found in read_versions(root).items()
        if found != expected
    ]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("version", nargs="?", help="New version, X.Y.Z.")
    parser.add_argument("--check", metavar="TAG", help="Fail unless every copy equals TAG.")
    args = parser.parse_args(argv)

    if args.check:
        problems = check(args.check)
        for problem in problems:
            print(f"Version mismatch: {problem}")
        return 1 if problems else 0
    if not args.version:
        parser.error("give a version to bump to, or --check TAG")
    bump(args.version)
    print(f"Bumped to {args.version}. Commit, then tag v{args.version}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""Bump or check the FridaForge version in every file that records it."""

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VERSION_FILE = Path("fridaforge") / "_version.py"
BINJA_MANIFEST = Path("plugin.json")
CORE_REQUIREMENT = "fridaforge"

_SEMVER = re.compile(r"\d+\.\d+\.\d+")
_VERSION_LINE = re.compile(r'__version__ = "([^"]*)"')


def stamp_binja_manifest(data: dict, version: str) -> dict:
    data["version"] = version
    pins = data.setdefault("dependencies", {}).setdefault("pip", [])
    others = [p for p in pins if not p.startswith(f"{CORE_REQUIREMENT}==")]
    data["dependencies"]["pip"] = [f"{CORE_REQUIREMENT}=={version}", *others]
    return data


def read_versions(root: Path = ROOT) -> dict[str, str]:
    match = _VERSION_LINE.search((root / VERSION_FILE).read_text(encoding="utf-8"))
    manifest = json.loads((root / BINJA_MANIFEST).read_text(encoding="utf-8"))
    pins = [
        p.split("==", 1)[1]
        for p in manifest.get("dependencies", {}).get("pip", [])
        if p.startswith(f"{CORE_REQUIREMENT}==")
    ]
    return {
        "_version.py": match.group(1) if match else "",
        "plugin.json version": manifest.get("version", ""),
        "plugin.json pip pin": pins[0] if pins else "",
    }


def bump(version: str, root: Path = ROOT) -> None:
    if not _SEMVER.fullmatch(version):
        raise ValueError(f"version must look like X.Y.Z, got {version!r}")
    (root / VERSION_FILE).write_text(
        f'__version__ = "{version}"\n', encoding="utf-8", newline="\n"
    )
    manifest_path = root / BINJA_MANIFEST
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    stamp_binja_manifest(data, version)
    manifest_path.write_text(
        json.dumps(data, indent=2) + "\n", encoding="utf-8", newline="\n"
    )


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

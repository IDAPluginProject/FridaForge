"""Assemble the two FridaForge host archives."""

import argparse
import json
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PKG = ROOT / "fridaforge"
HOSTS = ROOT / "hosts"
DIST = ROOT / "dist"
STAGING = ROOT / "build" / "_staging"

_IGNORE = shutil.ignore_patterns("__pycache__", "*.pyc")


def read_version() -> str:
    namespace: dict = {}
    exec((PKG / "_version.py").read_text(encoding="utf-8"), namespace)
    return namespace["__version__"]


def stamp_version(pkg_dir: Path, host: str, version: str) -> None:
    if host == "binja":
        path = pkg_dir / "plugin.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["version"] = version
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    else:
        path = pkg_dir / "ida-plugin.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["plugin"]["version"] = version
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def zip_folder(folder: Path, out: Path) -> None:
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as archive:
        for file in sorted(folder.rglob("*")):
            if file.is_file():
                arcname = file.relative_to(folder).as_posix()
                info = zipfile.ZipInfo(arcname, date_time=(1980, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o644 << 16
                archive.writestr(info, file.read_bytes())


def build_host(host: str, version: str, out_dir: Path = DIST) -> Path:
    stage = STAGING / host
    if stage.exists():
        shutil.rmtree(stage)
    stage.mkdir(parents=True)

    pkg_dir = stage / "fridaforge"
    shutil.copytree(PKG, pkg_dir, ignore=_IGNORE)

    for item in (HOSTS / host).iterdir():
        if item.is_file():
            shutil.copy2(item, pkg_dir / item.name)

    stamp_version(pkg_dir, host, version)

    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"fridaforge-{host}-{version}.zip"
    if out.exists():
        out.unlink()
    zip_folder(stage, out)
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description="Build FridaForge archives.")
    parser.add_argument("--version", default=None, help="Override version.")
    parser.add_argument(
        "--out-dir",
        default=None,
        help="Output directory for the archives (default: ./dist).",
    )
    args = parser.parse_args()
    version = args.version or read_version()
    out_dir = Path(args.out_dir).resolve() if args.out_dir else DIST

    for host in ("binja", "ida"):
        out = build_host(host, version, out_dir)
        print(f"Built {out}")


if __name__ == "__main__":
    main()

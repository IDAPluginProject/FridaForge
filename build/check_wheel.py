"""Fail if a built FridaForge wheel is missing core files or ships host code."""

import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FORBIDDEN_PREFIXES = ("hosts/", "tests/", "build/")


def expected_files() -> list[str]:
    package = ROOT / "fridaforge"
    return sorted(
        path.relative_to(ROOT).as_posix()
        for path in package.rglob("*")
        if path.is_file()
        and "__pycache__" not in path.parts
        and path.suffix in (".py", ".js")
    )


def check_wheel(path: Path) -> list[str]:
    with zipfile.ZipFile(path) as wheel:
        names = set(wheel.namelist())
    problems = [f"missing {name}" for name in expected_files() if name not in names]
    problems += [
        f"unexpected {name}" for name in sorted(names) if name.startswith(FORBIDDEN_PREFIXES)
    ]
    return problems


def main(argv: list[str]) -> int:
    if not argv:
        print("usage: check_wheel.py WHEEL [WHEEL ...]")
        return 2
    status = 0
    for arg in argv:
        problems = check_wheel(Path(arg))
        for problem in problems:
            print(f"{arg}: {problem}")
        status |= bool(problems)
    return status


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

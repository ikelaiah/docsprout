"""Qualification: verify the built wheel and sdist contain the complete product.

Run by CI after `python -m build`. Checks the declared version, module and
vendor-asset coverage, the console entry point, and sdist completeness without
installing anything.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
import tarfile
import zipfile


def _wheel_name(version: str) -> str:
    return f"dockit_fp-{version}-py3-none-any.whl"


def _sdist_name(version: str) -> str:
    return f"dockit_fp-{version}.tar.gz"


def _check_wheel(path: Path, version: str, failures: list[str]) -> int:
    with zipfile.ZipFile(path) as bundle:
        names = set(bundle.namelist())
        prefix = f"dockit_fp-{version}.dist-info/"
        expected_modules = (
            "__init__.py", "__main__.py", "archive.py", "assets.py", "audit.py",
            "build.py", "cli.py", "config.py", "discovery.py", "errors.py",
            "github_pages.py", "highlight.py", "markdown.py", "models.py",
            "safety.py", "versions.py",
        )
        for module in expected_modules:
            if f"dockit_fp/{module}" not in names:
                failures.append(f"wheel missing dockit_fp/{module}")
        katex = [name for name in names if name.startswith("dockit_fp/vendor/katex/")]
        for required in (
            "katex.min.js", "katex.min.css", "LICENSE", "fonts/KaTeX_Main-Regular.woff2",
        ):
            if f"dockit_fp/vendor/katex/{required}" not in names:
                failures.append(f"wheel missing KaTeX asset {required}")
        if len(katex) < 10:
            failures.append(f"wheel has only {len(katex)} KaTeX asset(s); expected the full bundled set")
        for meta in (f"{prefix}METADATA", f"{prefix}entry_points.txt", f"{prefix}RECORD"):
            if meta not in names:
                failures.append(f"wheel missing {meta}")
        entry_points = bundle.read(f"{prefix}entry_points.txt").decode("utf-8")
        if "dockit-fp = dockit_fp.cli:main" not in entry_points:
            failures.append("wheel entry point does not expose the dockit-fp command")
        metadata = bundle.read(f"{prefix}METADATA").decode("utf-8")
        if f"Version: {version}" not in metadata:
            failures.append("wheel METADATA version does not match the project")
        if "Requires-Python: >=3.10" not in metadata:
            failures.append("wheel METADATA requires-python does not match pyproject")
        for classifier in ("3.10", "3.11", "3.12", "3.13", "3.14"):
            if f"Programming Language :: Python :: {classifier}" not in metadata:
                failures.append(f"wheel METADATA lacks the Python {classifier} classifier")
        if "Requires-Dist:" in metadata:
            failures.append("wheel declares runtime dependencies; DocKit must stay dependency-free")
        return sum(1 for name in names if name.startswith("dockit_fp/") and name.endswith(".py"))


def _check_sdist(path: Path, version: str, failures: list[str]) -> int:
    with tarfile.open(path) as bundle:
        names = set(bundle.getnames())
        prefix = f"dockit_fp-{version}/"
        for required in (
            "pyproject.toml", "README.md", "src/dockit_fp/__init__.py", "src/dockit_fp/cli.py",
            "src/dockit_fp/vendor/katex/katex.min.js", "src/dockit_fp/vendor/katex/katex.min.css",
            "src/dockit_fp/vendor/katex/fonts/KaTeX_Main-Regular.woff2", "src/dockit_fp/vendor/katex/LICENSE",
        ):
            if prefix + required not in names:
                failures.append(f"sdist missing {required}")
        package_py = [name for name in names if name.startswith(prefix + "src/dockit_fp/") and name.endswith(".py")]
        if len(package_py) < 16:
            failures.append(f"sdist has only {len(package_py)} package modules")
        return len(package_py)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("dist_dir", type=Path)
    parser.add_argument("expected_version")
    arguments = parser.parse_args()
    failures: list[str] = []
    wheel = arguments.dist_dir / _wheel_name(arguments.expected_version)
    sdist = arguments.dist_dir / _sdist_name(arguments.expected_version)
    if not wheel.is_file():
        failures.append(f"missing wheel {_wheel_name(arguments.expected_version)}")
    if not sdist.is_file():
        failures.append(f"missing sdist {_sdist_name(arguments.expected_version)}")
    module_count = 0
    if wheel.is_file():
        module_count = _check_wheel(wheel, arguments.expected_version, failures)
    if sdist.is_file():
        _check_sdist(sdist, arguments.expected_version, failures)
    if failures:
        print(f"Artifact qualification FAILED for v{arguments.expected_version}:")
        for failure in failures:
            print(f"  - {failure}")
        return 1
    print(f"Artifact qualification passed: wheel and sdist for v{arguments.expected_version}; "
          f"{module_count} package modules with bundled KaTeX assets.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
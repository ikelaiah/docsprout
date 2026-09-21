"""Deterministic, offline documentation archives."""

from __future__ import annotations

import hashlib
from pathlib import Path
import zipfile


def write_offline_archive(site: Path, archive: Path, release: str) -> str:
    """Write a deterministic ZIP and matching SHA-256 sidecar."""
    site, archive = site.resolve(), archive.resolve()
    archive.parent.mkdir(parents=True, exist_ok=True)
    root = f"docsprout-docs-{release}"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
        for path in sorted(item for item in site.rglob("*") if item.is_file() and item.name not in {".docsprout-site", ".dockit-fp-site"}):
            info = zipfile.ZipInfo(f"{root}/{path.relative_to(site).as_posix()}")
            info.date_time = (1980, 1, 1, 0, 0, 0)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            bundle.writestr(info, path.read_bytes())
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    archive.with_name(archive.name + ".sha256").write_text(f"{digest}  {archive.name}\n", encoding="ascii")
    return digest

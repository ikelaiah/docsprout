"""Deprecated compatibility shim for the pre-rebrand ``dockit_fp`` package.

DocSprout is the canonical package. This shim keeps ``python -m dockit_fp``
and ``from dockit_fp import __version__`` working for at least one minor
release after the DocKit to DocSprout rename.
"""

from docsprout import __version__

__all__ = ["__version__"]

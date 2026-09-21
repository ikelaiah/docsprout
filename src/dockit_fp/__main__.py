"""Run the deprecated ``dockit_fp`` module entry point.

``python -m docsprout`` is the canonical form; this path is retained as a
deprecated alias for the 1.x compatibility window.
"""

import sys

from docsprout.cli import main

print("dockit_fp: deprecated module; use 'python -m docsprout' instead.", file=sys.stderr)
raise SystemExit(main(prog="dockit-fp"))

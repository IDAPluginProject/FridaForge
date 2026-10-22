"""Binary Ninja Extension Manager entry point. The plugin itself lives in hosts/binja."""

import sys

# Tools like pytest import the repo root as a package outside Binary Ninja.
# Binary Ninja imports its API before loading plugins, so only load then.
if "binaryninja" in sys.modules:
    from .hosts import binja  # noqa: F401

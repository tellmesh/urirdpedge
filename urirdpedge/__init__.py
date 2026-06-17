from __future__ import annotations

from .runtime import build_runtime, register_packs

__version__ = "0.1.0"


def register(rt):
    register_packs(rt)


__all__ = ["build_runtime", "register", "register_packs", "__version__"]

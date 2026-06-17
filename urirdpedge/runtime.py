from __future__ import annotations

import json
import os
from typing import Any

from urisysedge import compose
from urisysedge.runtime import Runtime, load_json, run_flow, serve
from urisysedge.env import load_urisys_env

DEFAULT_PACKS = "rdp,kvm,him,ocr,llm,shell,env,browser"


def _normalize_config(config: dict[str, Any]) -> dict[str, Any]:
    if not config:
        return {}
    if "kvm" not in config:
        drivers = config.get("drivers") or {}
        config.setdefault("kvm", {})
        screenshot_driver = drivers.get("screenshot", "mock")
        config["kvm"]["driver"] = screenshot_driver
        if config.get("screenshot_dir"):
            config["kvm"]["screenshot_dir"] = config["screenshot_dir"]
    if "ocr" not in config and (config.get("drivers") or {}).get("ocr"):
        config.setdefault("ocr", {})["driver"] = config["drivers"]["ocr"]
    if "llm" not in config and (config.get("drivers") or {}).get("llm"):
        config.setdefault("llm", {})["driver"] = config["drivers"]["llm"]
    return config


def _register_lab_browser(runtime: Runtime) -> None:
    from . import lab_browser

    lab_browser.register(runtime)


def _lab_browser_extra(packs):
    """The ``browser`` pack also needs the edge-local lab_browser routes."""
    names = packs.split(",") if isinstance(packs, str) else list(packs or [])
    names = {n.strip() for n in names}
    if "browser" in names or "uribrowserdocker" in names:
        return _register_lab_browser
    return None


def register_packs(rt: Runtime, *, packs: str | None = None, config: dict[str, Any] | None = None) -> None:
    """Register RDP desktop packs on an existing runtime (urisys-node hot-load)."""
    if config:
        rt.config.update(_normalize_config(config))
    names = packs or DEFAULT_PACKS
    compose.register_packs(rt, names)
    extra = _lab_browser_extra(names)
    if extra is not None:
        extra(rt)


def build_runtime(args) -> Runtime:
    config = _normalize_config(load_json(getattr(args, "config", None)))
    packs = getattr(args, "packs", DEFAULT_PACKS)
    return compose.build_runtime(
        packs=packs,
        bundle=getattr(args, "bundle", None),
        config=config,
        events_path=getattr(args, "events", "data/events.jsonl"),
        extra=_lab_browser_extra(packs),
    )


__all__ = ["Runtime", "build_runtime", "register_packs", "load_json", "run_flow", "serve", "load_urisys_env"]

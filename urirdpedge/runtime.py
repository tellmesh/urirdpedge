from __future__ import annotations

import json
import os
from typing import Any

from urisysedge.runtime import Runtime, load_json, run_flow, serve
from urisysedge.env import load_urisys_env


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


def _register_packs_on_runtime(rt: Runtime, packs: set[str]) -> None:
    if "rdp" in packs:
        import urirdp

        urirdp.register(rt)
    if "kvm" in packs:
        import urikvm

        urikvm.register(rt)
    if "him" in packs:
        import urihim

        urihim.register(rt)
    if "ocr" in packs:
        import uriocr

        uriocr.register(rt)
    if "llm" in packs:
        import urillm

        urillm.register(rt)
    if "shell" in packs:
        import urishell

        urishell.register(rt)
    if "env" in packs:
        import urienv

        urienv.register(rt)
    if "browser" in packs:
        import uribrowserdocker

        uribrowserdocker.register(rt)
        _register_lab_browser(rt)


def register_packs(rt: Runtime, *, packs: str | None = None, config: dict[str, Any] | None = None) -> None:
    """Register RDP desktop packs on an existing runtime (urisys-node hot-load)."""
    if config:
        rt.config.update(_normalize_config(config))
    pack_set = set(filter(None, (packs or "rdp,kvm,him,ocr,llm,shell,env,browser").split(",")))
    _register_packs_on_runtime(rt, pack_set)


def build_runtime(args) -> Runtime:
    config = _normalize_config(load_json(getattr(args, "config", None)))
    rt = Runtime(events_path=getattr(args, "events", "data/events.jsonl"), config=config)
    packs = set(filter(None, (getattr(args, "packs", "rdp,kvm,him,ocr,llm,shell,env,browser") or "").split(",")))
    _register_packs_on_runtime(rt, packs)
    return rt


__all__ = ["Runtime", "build_runtime", "register_packs", "load_json", "run_flow", "serve", "load_urisys_env"]

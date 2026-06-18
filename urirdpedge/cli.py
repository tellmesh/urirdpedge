from __future__ import annotations

import argparse
import json
import os

from uri_control.edge.http import serve as http_serve

from .runtime import build_runtime, load_json, load_urisys_env, run_flow


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="urisys-rdp")
    p.add_argument("--packs", default="rdp,kvm,him,ocr,llm,shell,env,browser")
    p.add_argument("--bundle", default=None, help="UriBundle Markpact; packs are derived from its imported contracts.")
    p.add_argument("--config", default=os.environ.get("URISYS_CONFIG", "config/rdp-kvm-profile.json"))
    p.add_argument("--events", default="data/events.jsonl")
    sub = p.add_subparsers(dest="cmd", required=True)

    c = sub.add_parser("call")
    c.add_argument("uri")
    c.add_argument("--payload", default="{}")
    c.add_argument("--approve", action="store_true")
    c.add_argument("--dry-run", action="store_true")
    c.add_argument("--allow-real", action="store_true")
    c.add_argument("--display", default=None)

    s = sub.add_parser("serve")
    s.add_argument("--host", default="0.0.0.0")
    s.add_argument("--port", type=int, default=8795)

    f = sub.add_parser("flow")
    f.add_argument("path")
    f.add_argument("--approve", action="store_true")
    f.add_argument("--dry-run", action="store_true")
    f.add_argument("--allow-real", action="store_true")
    f.add_argument("--display", default=None)

    args = p.parse_args(argv)
    load_urisys_env()
    rt = build_runtime(args)

    if args.cmd == "serve":
        http_serve(rt, args.host, args.port, service="urirdp")
        return 0

    context = {
        "approved": getattr(args, "approve", False),
        "dry_run": getattr(args, "dry_run", False),
        "allow_real": getattr(args, "allow_real", False),
    }
    if getattr(args, "display", None):
        context["display"] = args.display

    if args.cmd == "call":
        res = rt.call(args.uri, json.loads(args.payload), context)
        print(json.dumps(res, indent=2, ensure_ascii=False))
        return 0 if res.get("ok") else 1

    if args.cmd == "flow":
        res = run_flow(rt, args.path, context)
        print(json.dumps(res, indent=2, ensure_ascii=False))
        return 0 if all(r.get("ok") for r in res) else 1

    return 2


if __name__ == "__main__":
    raise SystemExit(main())

# urirdpedge

HTTP edge CLI (`urisys-rdp`) for RDP desktop automation — composes standalone URI packs on `uri_control.edge.Runtime``.

```bash
urisys-rdp \
  --config config/rdp-kvm-profile.json \
  --events data/events.jsonl \
  serve --host 0.0.0.0 --port 8795
```

## Packs loaded

| Alias | Package | Schemes |
|-------|---------|---------|
| rdp | `urirdp` | `rdp://` |
| kvm | `urikvm` | `kvm://` |
| him | `urihim` | `him://` |
| ocr | `uriocr` | `ocr://` |
| llm | `urillm` | `llm://` |
| shell | `urishell` | `shell://` |
| env | `urienv` | `env://` |
| browser | `uribrowserdocker` + lab aliases | `browser://` |

Lab browser aliases (`browser://{session}/page/open`, …) live in `urirdpedge.lab_browser`.

## Stack

```text
HTTP POST /uri/call
  → uri_control.edge.http.serve
  → `uri_control.edge.Runtime`
  → manifest-first packs (urirdp, urikvm, …)
```

Docker demo: [`urirdp-docker`](../urirdp-docker/).

Licensed under Apache-2.0.

## Ekosystem TellMesh

Orchestrator: **[urisys](https://github.com/tellmesh/urisys)** · Mapa: **[MESH.md](https://github.com/tellmesh/urisys/blob/main/docs/MESH.md)** · Model: **[ECOSYSTEM.md](https://github.com/tellmesh/urisys/blob/main/docs/ECOSYSTEM.md)**

| Pole | Wartość |
|------|---------|
| **Warstwa** | Edge CLI |
| **CLI** | `urisys-rdp` |
| **Runtime** | `uri_control.edge` (`uricontrol`) |
| **Packi** | urirdp, urikvm, urihim, urishell, uribrowser, … |
| **Port** | 8795 |

Runtime edge: **`uri_control.edge`** w pakiecie **`uricontrol`** (legacy PyPI `uricore` / `urisysedge` usunięty 2026-06).
Resolver intencji: **`uriresolver`** (`uri_resolver`) + transport w **`uritransport`**; policy gate: **`uriguard`** (`uri_guard`).

<!-- end-ecosystem -->

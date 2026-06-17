# urirdpedge

HTTP edge CLI (`urisys-rdp`) for RDP desktop automation — composes standalone URI packs on `urisysedge.Runtime`.

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
  → urisysedge.http.serve
  → urisysedge.Runtime
  → manifest-first packs (urirdp, urikvm, …)
```

Docker demo: [`urirdp-docker`](../urirdp-docker/).

Licensed under Apache-2.0.

# FridaForge

Generate ready-to-use [Frida](https://frida.re) instrumentation snippets directly
from **IDA Pro** and **Binary Ninja**. One codebase, two host adapters.

## Features

Right-click (or use a hotkey) in the disassembly/pseudocode view:

| Feature | Category | Hotkey |
| --- | --- | --- |
| Generate function hook | Hooks | `Shift+F` |
| Generate dlopen hooks (Android native libs) | Hooks | `Shift+D` |
| Modify current section permissions | Memory | `Shift+M` |
| Negate cond branch instruction (ARM64) | Patching | `Shift+A` |
| Negate cond branch instruction (x86) | Patching | `Shift+X` |

The generated snippet is copied to your clipboard.

## Installation

Download the archive for your tool from the
[latest release](https://github.com/noobexon1/FridaForge/releases) and unzip it
into the tool's plugins folder:

- **Binary Ninja:** unzip `fridaforge-binja-<version>.zip` so that
  `<binja user plugins>/fridaforge/` exists, then restart Binary Ninja.
- **IDA Pro:** unzip `fridaforge-ida-<version>.zip` so that
  `<IDA>/plugins/fridaforge/ida-plugin.json` exists, then restart IDA.

## Architecture

- `fridaforge/core` — host-agnostic snippet generators (template filling).
- `fridaforge/templates` — the Frida JS templates.
- `fridaforge/commands` — one `Command` per feature, talking only to a `Backend`.
- `fridaforge/backend.py` — the `Backend` interface implemented by each host.
- `hosts/binja`, `hosts/ida` — the host adapters (data extraction, clipboard,
  menu + hotkey registration).

## Building from source

```bash
pip install pytest
pytest -v
python build/build.py            # writes dist/fridaforge-binja-*.zip and dist/fridaforge-ida-*.zip
```

## License

MIT. See [LICENSE](LICENSE).

<div align="center">

# FridaForge

**Generate Frida scripts directly from IDA Pro and Binary Ninja.** ⚡

[![GitHub release](https://img.shields.io/github/v/release/noobexon1/FridaForge)](https://github.com/noobexon1/FridaForge/releases)
[![GitHub stars](https://img.shields.io/github/stars/noobexon1/FridaForge)](https://github.com/noobexon1/FridaForge/stargazers)
[![GitHub last commit](https://img.shields.io/github/last-commit/noobexon1/FridaForge)](https://github.com/noobexon1/FridaForge/commits)
[![GitHub issues](https://img.shields.io/github/issues/noobexon1/FridaForge)](https://github.com/noobexon1/FridaForge/issues)
[![GitHub downloads](https://img.shields.io/github/downloads/noobexon1/FridaForge/total)](https://github.com/noobexon1/FridaForge/releases)
[![Release](https://img.shields.io/github/actions/workflow/status/noobexon1/FridaForge/release.yml?label=release)](https://github.com/noobexon1/FridaForge/actions/workflows/release.yml)
![IDA Pro](https://img.shields.io/badge/IDA%20Pro-Plugin-blue)
![Binary Ninja](https://img.shields.io/badge/Binary%20Ninja-Plugin-orange)
![Frida](https://img.shields.io/badge/Frida-Instrumentation-red)
[![GitHub License](https://img.shields.io/github/license/noobexon1/FridaForge)](LICENSE)

*One codebase, two decompilers, zero boilerplate.* 🔥

</div>

## ✨ Features

Right-click (or hit a hotkey) in your disassembler to generate ready-to-use Frida snippets — the result is instantly copied to your clipboard.

- 🧩 **Composable scripts** — snippets are independent but can be nested to build complex instrumentation with a few clicks
- 🎯 **Context-aware** — scripts auto-fill module name, function address, section, and any other detail available from your current context
- 🧰 **Two hosts, one experience** — identical features, hotkeys, and menus in both IDA Pro and Binary Ninja
- 📋 **Clipboard integration** — generated scripts are copied the moment you run an action

### Supported Actions

#### 🪝 Hooks

| Action | Description | Hotkey |
|---|---|---|
| Generate function hook | Intercept calls to the selected function, log entry/exit | `Shift+F` |
| Generate dlopen hooks | Monitor `dlopen` (including Android variants) to detect module loading | `Shift+D` |

#### 🧠 Memory

| Action | Description | Hotkey |
|---|---|---|
| Modify section protection | Change memory protection of the section at the current address | `Shift+M` |

#### 🩹 Patching

| Action | Description | Hotkey |
|---|---|---|
| Negate cond branch (ARM64) | Flip the condition of an ARM64 conditional branch | `Shift+A` |
| Negate cond branch (x86/x64) | Flip the condition of an x86/x64 conditional branch | `Shift+X` |

## 🔧 How it Works

Each feature follows a simple pipeline: a **Frida template** (`fridaforge/templates/`) provides the JavaScript skeleton with placeholders, a **command** (`fridaforge/commands/`) gathers context through a host-agnostic **Backend**, and a **generator** (`fridaforge/core/`) fills the template to produce the final script.

The shared core knows nothing about IDA or Binary Ninja. Each host lives in `hosts/` and provides a thin **adapter** that implements the `Backend` interface (data extraction, clipboard, menu + hotkey registration). Add a feature once and it works in both tools.

## 📦 Installation

Download the archive for your tool from the [latest release](https://github.com/noobexon1/FridaForge/releases) and unzip it into the tool's plugins folder:

- 🟠 **Binary Ninja** — unzip `fridaforge-binja-<version>.zip` so that `<binja user plugins>/fridaforge/` exists, then restart Binary Ninja.

  Find your plugins directory with:
  ```python
  import binaryninja; print(binaryninja.user_plugin_path())
  ```
- 🔵 **IDA Pro** — unzip `fridaforge-ida-<version>.zip` so that `<IDA>/plugins/fridaforge/ida-plugin.json` exists, then restart IDA.

## 🚀 Usage

1. Open your target binary in IDA Pro or Binary Ninja.
2. Right-click in the disassembly or pseudocode view (or use the hotkeys above).
3. Navigate to **FridaForge** → choose a category and action.
4. The generated Frida script is copied to your clipboard.
5. Paste into your Frida CLI, agent, or `.js` file.

### 🧱 Script Composition

Snippets are designed to be independent building blocks. You can nest scripts inside each other — for example, hook a function, negate a conditional branch on entry, and restore it on exit. Complex instrumentation from a few clicks.

## 🛠️ Building from Source

```bash
pip install pytest
pytest -v                 # run the host-agnostic test suite
python build/build.py     # writes dist/fridaforge-binja-*.zip and dist/fridaforge-ida-*.zip
```

Builds are deterministic — the same source produces byte-identical archives.

## 🤝 Contributing

Contributions welcome! Got a useful Frida snippet? Turn it into a template so everyone can use it.

1. Fork the repository.
2. Create a new branch for your feature or fix.
3. Make your changes (and add a test — the core is fully unit-tested without needing a host).
4. Submit a pull request.

| Adding... | Where |
|---|---|
| New Frida snippet | `fridaforge/templates/` (JS template) + `fridaforge/core/` (generator) + `fridaforge/commands/` (command) |
| Host-specific behavior | `hosts/binja/` or `hosts/ida/` |

Each command and generator lives in its own file — easy to contribute without merge conflicts.

## 🗺️ Roadmap

See [open issues](https://github.com/noobexon1/FridaForge/issues) for planned features and known bugs.

## 📄 License

[MIT](LICENSE)

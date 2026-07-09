# Getting Started with eventhub-otlp-mapper

This guide is for people with **no coding experience**. It walks you through every step, from opening a terminal to running the mapper for the first time.

> **Before you start:** to see real data flowing, you need an Azure EventHub namespace with a **Listen** connection string, and somewhere to send the resulting traces/metrics (Grafana Cloud, Azure Monitor / Application Insights, or a local OpenTelemetry Collector). If you don't have those yet, you can still follow steps 1-4 below to get the tool installed; you'll just need real credentials before step 5 produces output.

---

## Windows

### 1. Open a terminal

Right-click the **Start** button and choose **Terminal** (or **Windows PowerShell** on older Windows versions).

### 2. Check your Python version

```powershell
py --version
```

- If it prints `Python 3.12.x` or higher, continue to step 3.
- If it prints an older version, or you see `'py' is not recognized as the name of a cmdlet, function, script file, or operable program`, Python isn't installed (or wasn't added to your system PATH).

**Install Python:**

1. Go to [python.org/downloads](https://www.python.org/downloads/) and download the latest installer.
2. Run it. On the very first screen, **check the box "Add python.exe to PATH"** at the bottom before clicking Install — this step is easy to miss and is the most common reason `py` isn't recognized afterwards.
3. Close and reopen your terminal, then re-run `py --version` to confirm.

### 3. Download eventhub-otlp-mapper

No-Git route:

1. Go to [github.com/9t29zhmwdh-coder/eventhub-otlp-mapper](https://github.com/9t29zhmwdh-coder/eventhub-otlp-mapper).
2. Click the green **Code** button → **Download ZIP**.
3. Extract it (right-click → **Extract All...**), e.g. to `Documents\eventhub-otlp-mapper`.

Or, with Git:

```powershell
git clone https://github.com/9t29zhmwdh-coder/eventhub-otlp-mapper.git
```

### 4. Move into the folder and install

```powershell
cd Documents\eventhub-otlp-mapper
pip install -e .
```

(Tip: type `cd ` with a trailing space, then drag the folder from File Explorer into the terminal to auto-fill the path. If `pip` isn't recognized, try `py -m pip install -e .` instead.)

### 5. Configure your credentials

```powershell
copy .env.example .env
notepad .env
```

Fill in, at minimum:
- `EVENTHUB_CONNECTION_STRING` — from your Azure EventHub namespace's shared access policy (must have **Listen** rights)
- `EVENTHUB_NAME` — the name of the specific EventHub inside that namespace
- `OTLP_ENDPOINT` — where traces/metrics should be sent (Grafana Cloud, a local OTel Collector, etc.)

Save and close Notepad.

### 6. Run it

```powershell
eventhub-otlp-mapper
```

If the command isn't recognized, run it via Python instead: `py -m eventhub_otel_mapper.main`.

---

## Linux

### 1. Open a terminal

Usually `Ctrl+Alt+T`, or search "Terminal" in your application menu.

### 2. Check your Python version

```bash
python3 --version
```

- `Python 3.12.x` or higher → continue to step 3.
- Older version or `command not found: python3` → most Linux distributions include Python already; if not, install it via your package manager, e.g. on Debian/Ubuntu:

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

### 3. Download eventhub-otlp-mapper

No-Git route: download the ZIP from [github.com/9t29zhmwdh-coder/eventhub-otlp-mapper](https://github.com/9t29zhmwdh-coder/eventhub-otlp-mapper) (green **Code** button → **Download ZIP**) and extract it.

Or, with Git:

```bash
git clone https://github.com/9t29zhmwdh-coder/eventhub-otlp-mapper.git
cd eventhub-otlp-mapper
```

### 4. Install

```bash
pip install -e .
```

If `pip` isn't found, try `pip3 install -e .` or `python3 -m pip install -e .`.

### 5. Configure your credentials

```bash
cp .env.example .env
nano .env
```

Fill in `EVENTHUB_CONNECTION_STRING`, `EVENTHUB_NAME`, and `OTLP_ENDPOINT` at minimum. Save with `Ctrl+O`, `Enter`, exit with `Ctrl+X`.

### 6. Run it

```bash
eventhub-otlp-mapper
```

---

## macOS

### 1. Open a terminal

Press `Cmd+Space`, type `Terminal`, press Enter.

### 2. Check your Python version

```bash
python3 --version
```

- `Python 3.12.x` or higher → continue to step 3.
- Older or `command not found: python3` → install from [python.org/downloads](https://www.python.org/downloads/) (run the installer with defaults), or via [Homebrew](https://brew.sh): `brew install python@3.12`. Then reopen Terminal and re-check.

### 3. Download eventhub-otlp-mapper

No-Git route: download the ZIP from [github.com/9t29zhmwdh-coder/eventhub-otlp-mapper](https://github.com/9t29zhmwdh-coder/eventhub-otlp-mapper) (green **Code** button → **Download ZIP**) and extract it (double-click in Finder).

Or, with Git:

```bash
git clone https://github.com/9t29zhmwdh-coder/eventhub-otlp-mapper.git
cd eventhub-otlp-mapper
```

### 4. Install

```bash
pip install -e .
```

If `pip` isn't found, try `pip3 install -e .` or `python3 -m pip install -e .`.

### 5. Configure your credentials

```bash
cp .env.example .env
nano .env
```

Fill in `EVENTHUB_CONNECTION_STRING`, `EVENTHUB_NAME`, and `OTLP_ENDPOINT` at minimum. Save with `Ctrl+O`, `Enter`, exit with `Ctrl+X`.

### 6. Run it

```bash
eventhub-otlp-mapper
```

<!-- TODO: Screenshot of a running consumer printing mapped spans -->

---

## What you should see

Once running with valid credentials, `eventhub-otlp-mapper` connects to your EventHub, starts consuming messages, and prints log lines as it maps each event to an OpenTelemetry span and sends it to your configured `OTLP_ENDPOINT`. Check your OTLP backend (Grafana, Application Insights, etc.) for the incoming traces.

The default field mapping lives in `config/mapping.yaml` — open it in any text editor to adjust which fields from your EventHub payloads become which OpenTelemetry attributes (see the "Mapping Example" section in the main [README.md](README.md)).

To stop the mapper, press `Ctrl+C` in the terminal it's running in.

---

### Troubleshooting

| Problem | Cause | Fix |
|---|---|---|
| Windows: `'py' is not recognized...` | Python isn't installed, or wasn't added to PATH during install | Reinstall from [python.org](https://www.python.org/downloads/), ticking "Add python.exe to PATH", then reopen the terminal |
| Linux/macOS: `command not found: python3` | Python isn't installed | Linux: `sudo apt install python3` (Debian/Ubuntu) or your distro's equivalent. macOS: install from [python.org](https://www.python.org/downloads/) or `brew install python@3.12` |
| `eventhub-otlp-mapper` fails immediately with an authentication/connection error | `EVENTHUB_CONNECTION_STRING` in `.env` is missing, wrong, or lacks Listen rights | Double-check the connection string in the Azure Portal under your EventHub namespace's **Shared access policies**, and confirm it has **Listen** permission |
| No traces appear in your OTLP backend | `OTLP_ENDPOINT` is wrong, unreachable, or the backend needs an API key | Verify the endpoint URL and, if required, set `OTLP_API_KEY` in `.env`; see [`docs/azure_integration.md`](docs/azure_integration.md) for backend-specific setup |
| Windows PowerShell blocks running a `.ps1` script with "cannot be loaded because running scripts is disabled on this system" | PowerShell's execution policy blocks unsigned local scripts | Only if you intentionally need to run a `.ps1` helper script: open PowerShell as Administrator and run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, then confirm with `Y` |

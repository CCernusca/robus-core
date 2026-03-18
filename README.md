# robus-core
Core connection component of the bot controlling system, which provides the infrastructure for framework nodes to communicate via Redis.

## How it works

- **Nodes** are Python scripts named `node_*.py`, placed in the **parent directory** of `robus-core/`
- Each node communicates with others through a shared Redis instance using the `TelemetryBroker` library (`libs/lib_telemtrybroker.py`)
- `utils/detect_nodes.py` scans for nodes and writes their paths to `tmp/node_list.csv`
- `utils/starter.py` detects and launches all nodes, each in its own terminal window
- To disable a node without deleting it, prefix its filename with `_` (e.g. `_node_sensor.py`)

## Directory structure

```
robus-core/
├── libs/               # Shared libraries (TelemetryBroker, sensor drivers)
├── setup/              # Setup and launch scripts
├── tmp/                # Runtime output (gitignored)
└── utils/              # Core scripts (starter, stop, node detection)

../                     # Parent directory — place node_*.py files here
```

## Setup

### 1. Install Redis (Linux)

```bash
bash setup/setup_redis.sh
```

### 2. Configure autostart (optional)

**Linux:**
```bash
bash setup/configure_startup.sh
```

**Windows:**
```bat
setup\configure_startup.bat
```

## Running

### Start all nodes

**Linux:**
```bash
bash setup/start.sh
```

**Windows:**
```bat
setup\start.bat
```

This activates the virtual environment if one is found at `venv/` or `env/`, then launches `utils/starter.py`.

### Stop all nodes

```bash
python utils/stop.py
```

## Virtual environment

If a virtual environment exists at `robus-core/venv/` or `robus-core/env/`, the start scripts activate it automatically. To create one:

```bash
python -m venv venv
venv/Scripts/activate      # Windows
source venv/bin/activate   # Linux

pip install redis psutil
```

# robus-core

Core connection component of the bot controlling system, which provides the infrastructure for framework nodes to communicate via Redis.

## How it works

- **Nodes** are Python scripts named `node_*.py`, placed in the **parent directory** of `robus-core/`
- Each node communicates with others through a shared Redis instance using the `TelemetryBroker` library (`libs/lib_telemtrybroker.py`)
- `utils/detect_nodes.py` scans for nodes and writes their paths to `tmp/node_list.csv`
- `utils/starter.py` detects and launches all nodes, each in its own terminal window
- To disable a node without deleting it, prefix its filename with `_` (e.g. `_node_sensor.py`)

## Directory structure

```markdown
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

---

## Creating a Node

A node is a standalone Python script that communicates with other nodes via Redis.

### 1. Create the file

- The filename must start with `node_`: e.g. `node_sensor.py`
- The file belongs in the **parent directory** of `robus-core/`:

```bash
my-project/
├── robus-core/       ← framework
├── node_sensor.py    ← your node
└── node_motor.py     ← your node
```

> Prefixing a filename with `_` (e.g. `_node_sensor.py`) excludes the node from autostart without deleting it.

### 2. Import TelemetryBroker

```python
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "robus-core"))

from libs.lib_telemtrybroker import TelemetryBroker

broker = TelemetryBroker()          # connects to localhost:6379
# broker = TelemetryBroker(host="...", port=6379, db=0)  # optional
```

The broker automatically registers the node in Redis on startup. The key name is the filename without `.py`.

### 3. Writing data

```python
broker.set("motor_speed", 42)
broker.set("status", "running")
broker.set("armed", True)           # bool is automatically cast to int (0/1)

broker.setmulti({
    "x": 1.5,
    "y": -3.0,
    "z": 0.0,
})
```

### 4. Reading data

```python
speed = broker.get("motor_speed")          # single value
data  = broker.getmulti(["x", "y", "z"])   # multiple values → dict
all   = broker.getall()                     # entire Redis contents → dict
imu   = broker.getallWith("imu_*")         # all keys matching a prefix → dict
```

Values are automatically cast to `int`, `float`, or `str` depending on their content.

### 5. Reacting to changes (callback)

```python
def on_change(key, value):
    print(f"{key} changed: {value}")

broker.setcallback(["motor_speed", "armed"], on_change)
broker.receiver_loop()   # blocking — call at the end of main()
```

`receiver_loop()` runs indefinitely and invokes the callback whenever a monitored value changes.

### 6. Permissions

| Value | Meaning                              |
|-------|--------------------------------------|
| `0`   | No access                            |
| `1`   | Read only                            |
| `2`   | Read, write, delete (default)        |

```python
broker.get_node_permission()   # returns 0, 1, or 2
```

The default is `2`. Another node can restrict permissions via `broker.set("node_sensor", 1)`.

### 7. Minimal example

```python
import sys, os, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "robus-core"))
from libs.lib_telemtrybroker import TelemetryBroker

broker = TelemetryBroker()

while True:
    broker.set("sensor_value", 42)
    print(broker.getall())
    time.sleep(0.1)
```

### 8. Cleanup

The `TelemetryBroker` destructor calls `close()` automatically, which removes the node's key from Redis. To call it explicitly:

```python
broker.close()
```

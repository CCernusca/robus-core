#!/bin/bash
# Activates the Python virtual environment (if present) and starts starter.py.

ROBUS_CORE="$(cd "$(dirname "$0")/.." && pwd)"

if [ -f "$ROBUS_CORE/venv/bin/activate" ]; then
    echo "Activating venv..."
    source "$ROBUS_CORE/venv/bin/activate"
elif [ -f "$ROBUS_CORE/env/bin/activate" ]; then
    echo "Activating env..."
    source "$ROBUS_CORE/env/bin/activate"
else
    echo "No virtual environment found, using system Python."
fi

python "$ROBUS_CORE/utils/starter.py"

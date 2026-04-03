#!/bin/bash
# Activates the Python virtual environment (if present) and starts starter.py.

ROBUS_CORE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PARENT="$(dirname "$ROBUS_CORE")"

ACTIVATE=""
VENV_PATH=""
for BASE in "$ROBUS_CORE" "$PARENT"; do
    for NAME in venv env; do
        for BINDIR in bin Scripts; do
            CANDIDATE="$BASE/$NAME/$BINDIR/activate"
            if [ -f "$CANDIDATE" ]; then
                ACTIVATE="$CANDIDATE"
                VENV_PATH="$BASE/$NAME"
                break 3
            fi
        done
    done
done

if [ -n "$ACTIVATE" ]; then
    echo "Activating venv: $VENV_PATH"
    source "$ACTIVATE"
else
    echo "No virtual environment found. Checked:"
    for BASE in "$ROBUS_CORE" "$PARENT"; do
        for NAME in venv env; do
            echo "  $BASE/$NAME"
        done
    done
    echo "Using system Python."
fi

# Install Python dependencies if requirements.txt exists
REQ_FILE="$ROBUS_CORE/../requirements.txt"

if [ -f "$REQ_FILE" ]; then
    echo "Installing Python dependencies from $REQ_FILE"
    python3 -m pip install --upgrade pip
    python3 -m pip install -r "$REQ_FILE"
else
    echo "No requirements.txt found at $REQ_FILE"
fi

# Run Redis setup script if present
SETUP_SCRIPT="$ROBUS_CORE/setup/setup_redis.sh"
if [ -f "$SETUP_SCRIPT" ]; then
    echo "Running Redis setup: $SETUP_SCRIPT"
    bash "$SETUP_SCRIPT"
else
    echo "No setup_redis.sh found at $SETUP_SCRIPT"
fi

python3 "$ROBUS_CORE/utils/starter.py"

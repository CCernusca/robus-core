#!/bin/bash
# Activates the Python virtual environment (if present) and starts starter.py.

ROBUS_CORE="$(cd "$(dirname "$0")/.." && pwd)"
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

python "$ROBUS_CORE/utils/starter.py"

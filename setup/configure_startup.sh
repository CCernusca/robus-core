#!/bin/bash
# Configures Linux autostart to run starter.py at user login.
# Creates ~/.config/autostart/nodestarter.desktop

STARTER_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/utils/starter.py"
DESKTOP_FILE="$HOME/.config/autostart/nodestarter.desktop"

mkdir -p "$HOME/.config/autostart"

cat > "$DESKTOP_FILE" <<EOF
[Desktop Entry]
Type=Application
Name=Node Starter
Exec=python3 "$STARTER_PATH"
Terminal=true
EOF

echo "Autostart entry created at $DESKTOP_FILE"
echo "starter.py will launch automatically at next login."

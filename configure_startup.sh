#!/bin/bash
# Configures Linux autostart to run start.sh at user login.
# Creates ~/.config/autostart/nodestarter.desktop

STARTER_PATH="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/setup/start.sh"
DESKTOP_FILE="$HOME/.config/autostart/nodestarter.desktop"

mkdir -p "$HOME/.config/autostart"

chmod +x "$STARTER_PATH"

cat > "$DESKTOP_FILE" <<EOF
[Desktop Entry]
Type=Application
Name=Node Starter
Exec=/bin/bash -lc "$STARTER_PATH"
Terminal=true
X-GNOME-Autostart-enabled=true
EOF

echo "Autostart entry created at $DESKTOP_FILE"
echo "start.sh will launch automatically at next login."

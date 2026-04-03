# TelemetryBroker for Inter Process Communication for Robtics
# Starter for all Nodes
# Developed by Martin Novak at 2025/26
#   - Nodes must be in the parent folder of robus-core
#   - Filename must be start with "node_", example "node_sensor.py"
#   - To deactivate autostart for a file, rename it, example "_node_sensor.py"
# Autostart script installation:
#   1 - sudo nano ~/.config/autostart/nodestarter.desktop
#   2 - Insert following lines:
#       [Desktop Entry]
#       Type=Application
#       Name=Node Starter
#       Exec=python3 /home/pi/desktop/starter.py
#       Terminal=true
import os
import sys
import subprocess
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from libs.lib_telemtrybroker import TelemetryBroker
import utils.detect_nodes as detect_nodes

#time.sleep(5)

print("Waiting for Redis connection:")
wait_on_redis = True
while wait_on_redis:
    try:
        print("Trying to connect to Redis... ", end="")
        mb = TelemetryBroker()
        wait_on_redis = False
    except:
        pass

mb.clearall()

files = detect_nodes.detect()

print("Start of", len(files), "nodes")

python_exec = sys.executable

for file in files:
    print(file)

    if os.name == 'posix':
        #LINUX:
        command = f'"{python_exec}" "{file}"; echo "Script finished. Press Enter to close..."; read'
        subprocess.Popen(["lxterminal", "--command", f"bash -c '{command}'"])

    elif os.name == 'nt':
        #WINDOWS:
        command = f'"{python_exec}" "{file}"'
        subprocess.Popen(f'start cmd /k "{command}"', shell=True)
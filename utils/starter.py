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
import shutil

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from libs.lib_telemtrybroker import TelemetryBroker
import utils.detect_nodes as detect_nodes

DEBUG = any(arg.lower() == "--debug" for arg in sys.argv)

# Parse --no-output: node names listed here keep their output; all others get --no-output
no_output_exceptions = []
if "--no-output" in sys.argv:
    idx = sys.argv.index("--no-output")
    for arg in sys.argv[idx + 1:]:
        if arg.startswith("--"):
            break
        no_output_exceptions.append(arg)

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

    node_name = os.path.splitext(os.path.basename(file))[0]
    no_output_flag = "" if node_name in no_output_exceptions else " --no-output"
 
    if os.name == 'posix':
        #LINUX:
        command = f'"{python_exec}" "{file}"{no_output_flag}; echo "Script finished. Press Enter to close..."; read'

        terminal = None
        for t in ["lxterminal", "gnome-terminal", "konsole", "x-terminal-emulator"]:
            if shutil.which(t):
                terminal = t
                break

        if terminal:
            if terminal == "gnome-terminal":
                subprocess.Popen([terminal, "--", "bash", "-c", command])
            elif terminal == "konsole":
                subprocess.Popen([terminal, "-e", "bash", "-c", command])
            else:
                subprocess.Popen([terminal, "-e", f"bash -c '{command}'"])
        else:
            print("No GUI terminal found → running in background")
            subprocess.Popen(command, shell=True)

    elif os.name == 'nt':
        # WINDOWS:
        command = f'"{python_exec}" "{file}"{no_output_flag}'

        # Use /k in debug mode (keeps terminal open), otherwise /c
        cmd_flag = "/k" if DEBUG else "/c"

        subprocess.Popen(f'start cmd {cmd_flag} "{command}"', shell=True)
# TelemetryBroker for Inter Process Communication for Robtics
# KILL all running Nodes
# Developed by Martin Novak at 2025/26
# pip install psutil

import psutil
import os


def auto_kill_node_scripts():
    # Get own PID so the script does not terminate itself
    own_pid = os.getpid()
    found_processes = 0

    print("Searching for running Python scripts starting with 'node'...")

    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = proc.info.get('cmdline')

            # Skip processes without a command line (e.g. system kernel)
            if not cmdline or len(cmdline) < 2:
                continue

            # Check:
            # 1. Is it a Python process?
            # 2. Does the first argument (the script) start with 'node'?
            script_path = cmdline[1]
            script_name = os.path.basename(script_path)

            if "python" in proc.info['name'].lower() and script_name.startswith("node"):
                if proc.info['pid'] != own_pid:
                    print(f"[*] Terminating: {script_name} (PID: {proc.info['pid']})")
                    proc.terminate()
                    found_processes += 1

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    if found_processes == 0:
        print("[i] No matching scripts found.")
    else:
        print(f"[!] Stopped {found_processes} script(s) in total.")

if __name__ == "__main__":
    auto_kill_node_scripts()
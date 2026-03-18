# TelemetryBroker for Inter Process Communication for Robtics
# Node Detection - scans for node scripts and writes their paths to tmp/node_list.csv
# Developed by Martin Novak at 2025/26

import os
import glob
import csv

ROBUS_CORE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEARCH_PATH = os.path.dirname(ROBUS_CORE)
MUSTER = "node_*.py"
NODE_LIST_CSV = os.path.join(ROBUS_CORE, "tmp", "node_list.csv")


def detect():
    files = [os.path.abspath(f) for f in glob.glob(os.path.join(SEARCH_PATH, MUSTER))]
    os.makedirs(os.path.dirname(NODE_LIST_CSV), exist_ok=True)
    with open(NODE_LIST_CSV, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["path"])
        for file in files:
            writer.writerow([file])
    print(f"Detected {len(files)} nodes, written to {NODE_LIST_CSV}")
    return files


if __name__ == "__main__":
    detect()

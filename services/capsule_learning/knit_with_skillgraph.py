#!/usr/bin/env python3
import os, json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
CORTEX_FILE = os.path.join(BASE_DIR, "knowledge", "compiled_capsules", "warehouse_ops.cortex.json")

def main():
    if not os.path.exists(CORTEX_FILE):
        print("⚠️ No compiled capsule found")
        return
    with open(CORTEX_FILE) as f:
        cortex = json.load(f)
    # example: attach an audit log
    cortex["governance"]["knit_with_skillgraph"] = True
    cortex["governance"]["policy_override"] = None
    with open(CORTEX_FILE, "w") as f:
        json.dump(cortex, f, indent=2)
    print("Knitting complete: added skillgraph links.")

if __name__ == "__main__":
    main()

"""
capsule_cortex.py
Provides class interface to load and access CapsuleCortex.
"""

import json

class CapsuleCortex:
    def __init__(self, path):
        with open(path) as f:
            self.data = json.load(f)

    def get_region(self, region):
        return self.data["regions"].get(region, {})

    def list_micro_steps(self):
        return [s["op"] for s in self.data["micro_steps"]]

if __name__ == "__main__":
    cc = CapsuleCortex("knowledge/compiled_capsules/warehouse_ops.cortex.json")
    print(cc.list_micro_steps())

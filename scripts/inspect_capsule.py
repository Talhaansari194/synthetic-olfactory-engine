"""
inspect_capsule.py
Pretty prints Cortex nodes and edges.
"""
import json

def inspect(path="knowledge/compiled_capsules/warehouse_ops.cortex.json"):
    data = json.load(open(path))
    print("Role:", data["role"])
    print("Regions:", list(data["regions"].keys()))
    print("Micro-steps:")
    for s in data["micro_steps"]:
        print("  →", s)

if __name__ == "__main__":
    inspect()

"""
action_planner.py
Reads CapsuleCortex and prints planned steps.
"""
import json

def plan_from_capsule(cortex_path="knowledge/compiled_capsules/warehouse_ops.cortex.json"):
    cortex = json.load(open(cortex_path))
    print("Planned micro-steps:")
    for step in cortex["micro_steps"]:
        print(f" - {step['op']} {step['params']}")

if __name__ == "__main__":
    plan_from_capsule()

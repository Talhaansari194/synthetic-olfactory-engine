#!/usr/bin/env python3
import json, os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CORTEX = os.path.join(BASE_DIR, "knowledge", "compiled_capsules", "warehouse_ops.cortex.json")

def test_planner_capsule_influence():
    """capsule adds VERIFY_PPE pre-check step"""
    cortex = json.load(open(CORTEX))
    plan = cortex["mappings"]["scenarios"]["methane_leak_hazard"]
    assert "VERIFY_PPE" in plan or any("PPE" in p for p in plan), \
        "Capsule influence missing (no VERIFY_PPE step)"
    print("✅ Capsule influence test passed")

if __name__ == "__main__":
    test_planner_capsule_influence()

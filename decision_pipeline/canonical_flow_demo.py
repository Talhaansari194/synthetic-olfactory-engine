#!/usr/bin/env python3
import json, os, time

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CTX_FILE = os.path.join(BASE_DIR, "knowledge", "compiled_capsules", "warehouse_ops.cortex.json")
TRACE_FILE = os.path.join(BASE_DIR, "knowledge", "scenario_trace.jsonl")

def simulate_packet(packet):
    print(f"\n⚙️  Received canonical packet: {packet}")
    hazard = "methane_leak_hazard"
    print(f"→ Classifier labels: {hazard}")
    role = "warehouse_ops"
    cortex = json.load(open(CTX_FILE))
    plan = cortex["mappings"]["scenarios"][hazard]
    print(f"→ CapsuleCortex plan: {plan}")
    for step in plan:
        print(f"   executing {step} ...")
        time.sleep(0.2)
    with open(TRACE_FILE, "a") as f:
        f.write(json.dumps({"timestamp": time.time(), "packet": packet, "executed": plan}) + "\n")
    print("→ Scenario trace recorded.")

if __name__ == "__main__":
    simulate_packet({"gas":"CH4","ppm":123})

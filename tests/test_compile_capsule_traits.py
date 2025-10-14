#!/usr/bin/env python3
import json, os, time, statistics

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
CORTEX = os.path.join(BASE_DIR, "knowledge", "compiled_capsules", "warehouse_ops.cortex.json")

def test_latency_and_safety():
    """latency ≤ 10 ms p95 + params in bounds"""
    cortex = json.load(open(CORTEX))
    # latency
    samples = []
    for _ in range(100):
        t0 = time.perf_counter()
        _ = cortex["regions"]["Hippocampus"]["episodic_sequences"]
        samples.append((time.perf_counter() - t0) * 1000)
    p95 = statistics.quantiles(samples, n=100)[94]
    assert p95 <= 10.0, f"Capsule lookup latency {p95:.2f} ms > 10 ms"
    print(f"Latency p95 = {p95:.2f} ms ✅")

    # safety bounds
    for step in cortex.get("micro_steps", []):
        p = step.get("params", {})
        if "meters" in p:
            assert 0 <= p["meters"] <= 100, f"meters out of range {p['meters']}"
        if "duration_s" in p:
            vals = p["duration_s"] if isinstance(p["duration_s"], list) else [p["duration_s"]]
            for v in vals:
                assert 0 <= v <= 900, f"duration out of range {v}"
    print("✅ Safety bounds check passed")

if __name__ == "__main__":
    test_latency_and_safety()

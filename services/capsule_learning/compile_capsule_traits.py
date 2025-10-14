#!/usr/bin/env python3
import json
import os
import hashlib

# --------------------------------------------------------------------
# Utility to hash IDs (for AU naming consistency)
# --------------------------------------------------------------------
def hash_text(text):
    return hashlib.md5(text.encode()).hexdigest()[:8]

# --------------------------------------------------------------------
# Input & output paths
# --------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
AU_SEGMENTS_FILE = os.path.join(BASE_DIR, "knowledge", "training_sources", "au_segments.jsonl")
OUTPUT_FILE = os.path.join(BASE_DIR, "knowledge", "compiled_capsules", "warehouse_ops.cortex.json")

# --------------------------------------------------------------------
# Load Action Units (AUs)
# --------------------------------------------------------------------
au_segments = []
if os.path.exists(AU_SEGMENTS_FILE):
    with open(AU_SEGMENTS_FILE, "r") as f:
        for line in f:
            try:
                au_segments.append(json.loads(line))
            except json.JSONDecodeError:
                continue
else:
    print(f"⚠️ Warning: {AU_SEGMENTS_FILE} not found. Using empty list.")
    au_segments = []

# --------------------------------------------------------------------
# Extract AU IDs and Tags
# --------------------------------------------------------------------
au_ids = [au.get("au_id") for au in au_segments if "au_id" in au]
ppe_tags = [au for au in au_segments if "PPE" in au.get("tags", [])]

# --------------------------------------------------------------------
# Build Capsule Cortex
# --------------------------------------------------------------------
capsule = {
    "role": "warehouse_ops",
    "cortex_id": "CTX-WAREHOUSE-OPS-v1",
    "regions": {
        "Hippocampus": {
            "episodic_sequences": au_ids,
            "recency_bias": 0.7
        },
        "Amygdala": {
            "risk_heuristics": [
                {"scent_id": "H2S-SUL-003", "ppm_gte": 10, "risk": "high", "response": "evacuate_area"},
                {"scent_id": "METHANE-CH4-007", "ppm_gte": 25, "risk": "medium", "response": "ventilate_and_alert"}
            ]
        },
        "OFC": {
            "tradeoffs": [
                {"name": "vent_vs_egress", "weight": 0.6},
                {"name": "speed_vs_safety", "weight": 0.4}
            ]
        },
        # ✅ FIXED SECTION: Wrap PFC as an object with planning_templates
        "PFC": {
            "planning_templates": au_ids  # previously: PFC = [list], now object
        },
        "OlfactoryCortex": {
            "cue_binding": [
                {"class": "sulfur", "cue_nodes": ["AU-H2S-PPE", "AU-H2S-BACKOFF"]},
                {"class": "methane", "cue_nodes": ["AU-METHANE-VENT", "AU-METHANE-ALERT"]},
                {"class": "smoke", "cue_nodes": ["AU-FIRE-ALERT", "AU-FIRE-EVAC"]}
            ]
        }
    },
    "micro_steps": [],
    "mappings": {
        "scenarios": {
            "methane_leak_hazard": ["PRECHECK_PPE", "VERIFY_VENTILATION", "BACKOFF_10M", "ALERT_SUPERVISOR"],
            "h2s_spike": ["PRECHECK_PPE", "BACKOFF_10M", "ALERT_SUPERVISOR"]
        },
        "skillgraph_links": {
            "VENTILATION_PROCEDURE": ["VERIFY_VENTILATION"],
            "EMERGENCY_RESPONSE": ["ALERT_SUPERVISOR", "BACKOFF_10M"]
        }
    },
    "governance": {
        "sandbox": True,
        "version": "v1",
        "created_by": "compile_capsule_traits.py",
        "firewall_checked": True
    }
}

# --------------------------------------------------------------------
# Derive micro-steps from AU content
# --------------------------------------------------------------------
for au in ppe_tags:
    ppe_items = au.get("entities", {}).get("ppe", [])
    for item in ppe_items:
        capsule["micro_steps"].append({
            "id": f"VERIFY_PPE_{au.get('au_id', hash_text(item))}",
            "op": "VERIFY_PPE",
            "params": {"item": item}
        })

# --------------------------------------------------------------------
# Write Output
# --------------------------------------------------------------------
os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
with open(OUTPUT_FILE, "w") as f:
    json.dump(capsule, f, indent=2)

print(f"Compiled capsule written to {OUTPUT_FILE}")

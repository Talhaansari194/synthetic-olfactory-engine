#!/usr/bin/env python3
import os, json, re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
AU_FILE = os.path.join(BASE_DIR, "knowledge", "training_sources", "au_segments.jsonl")
COG_MAP_FILE = os.path.join(BASE_DIR, "configs", "cognition_map.json")
OUT_FILE = os.path.join(BASE_DIR, "knowledge", "training_sources", "cognitive_graph.json")

def main():
    if not os.path.exists(AU_FILE) or not os.path.exists(COG_MAP_FILE):
        print("⚠️ Required files missing")
        return
    with open(COG_MAP_FILE) as f: cmap = json.load(f)
    with open(AU_FILE) as f: aus = [json.loads(l) for l in f]

    regions = {r: [] for r in ["Hippocampus","Amygdala","OFC","PFC"]}
    for au in aus:
        utt = au["utterance"].lower()
        for verb, region in cmap["verb_to_region"].items():
            if re.search(rf"\b{verb}\b", utt):
                regions[region].append(au["au_id"])
                break
    with open(OUT_FILE,"w") as f: json.dump(regions,f,indent=2)
    print(f"Derived cognitive graph with {sum(len(v) for v in regions.values())} nodes.")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import os, json, re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
AU_FILE = os.path.join(BASE_DIR, "knowledge", "training_sources", "au_segments.jsonl")
OUT_FILE = os.path.join(BASE_DIR, "knowledge", "training_sources", "checklists.json")

ppe_lexicon = ["respirator_p100","scba","gloves","goggles"]

def main():
    if not os.path.exists(AU_FILE):
        print("⚠️ au_segments.jsonl not found")
        return
    checklists = []
    with open(AU_FILE) as f:
        for line in f:
            au = json.loads(line)
            text = au["utterance"].lower()
            ppe_found = [p for p in ppe_lexicon if p in text]
            if ppe_found:
                checklists.append({
                    "au_id": au["au_id"],
                    "op": "VERIFY_PPE",
                    "params": {"item": ppe_found[0]}
                })
    with open(OUT_FILE, "w") as f:
        json.dump(checklists, f, indent=2)
    print(f"Extracted checklists from {len(checklists)} AUs.")

if __name__ == "__main__":
    main()

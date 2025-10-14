#!/usr/bin/env python3
import os, json, hashlib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
INPUT_FILE = os.path.join(BASE_DIR, "knowledge", "training_sources", "normalized_transcripts.json")
OUTPUT_FILE = os.path.join(BASE_DIR, "knowledge", "training_sources", "au_segments.jsonl")

imperatives = ["check","verify","don","open","close","evacuate","alert","isolate","shut","ventilate"]

def hash_line(line): return hashlib.md5(line.encode()).hexdigest()[:8]

def main():
    if not os.path.exists(INPUT_FILE):
        print("⚠️ normalized_transcripts.json not found")
        return

    with open(INPUT_FILE) as f: data = json.load(f)
    count = 0
    with open(OUTPUT_FILE, "w") as out:
        for src, lines in data.items():
            for i, line in enumerate(lines):
                au = {
                    "au_id": f"AU-{hash_line(line)}",
                    "source_id": f"yt:{src.replace('.txt','')}",
                    "t_start_s": i*5.0,
                    "t_end_s": i*5.0 + 3.0,
                    "utterance": line,
                    "tags": [w.upper() for w in imperatives if w in line.lower()],
                    "entities": {},
                    "preconditions": [],
                    "postconditions": [],
                    "confidence": 0.9
                }
                out.write(json.dumps(au) + "\n")
                count += 1
    print(f"Segmented {count} action units.")

if __name__ == "__main__":
    main()

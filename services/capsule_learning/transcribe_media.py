#!/usr/bin/env python3
import os, json, re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
TRANSCRIPTS_DIR = os.path.join(BASE_DIR, "knowledge", "training_sources", "transcripts")
OUT_FILE = os.path.join(BASE_DIR, "knowledge", "training_sources", "normalized_transcripts.json")

imperatives = ["check","verify","don","open","close","evacuate","alert","isolate","shut","ventilate"]

def clean_line(line):
    line = re.sub(r"[^a-zA-Z0-9, ]", " ", line)
    return " ".join(line.strip().split())

def main():
    out = {}
    for fn in os.listdir(TRANSCRIPTS_DIR):
        if not fn.endswith(".txt"): 
            continue
        with open(os.path.join(TRANSCRIPTS_DIR, fn)) as f:
            lines = [clean_line(l) for l in f if any(v in l.lower() for v in imperatives)]
            out[fn] = lines
    with open(OUT_FILE, "w") as f:
        json.dump(out, f, indent=2)
    print(f"Normalized {len(out)} transcript(s)")

if __name__ == "__main__":
    main()

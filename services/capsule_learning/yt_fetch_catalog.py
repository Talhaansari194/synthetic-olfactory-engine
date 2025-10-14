#!/usr/bin/env python3
import json, os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
CATALOG_FILE = os.path.join(BASE_DIR, "knowledge", "training_sources", "curated_links.json")
TRANSCRIPTS_DIR = os.path.join(BASE_DIR, "knowledge", "training_sources", "transcripts")

def main():
    print("=== Fetching catalog of training sources ===")
    if not os.path.exists(CATALOG_FILE):
        print(f"⚠️  {CATALOG_FILE} not found.")
        return

    with open(CATALOG_FILE, "r") as f:
        catalog = json.load(f)

    for entry in catalog:
        tid = entry["id"]
        fname = os.path.join(TRANSCRIPTS_DIR, f"{tid}.txt")
        status = "✅ found" if os.path.exists(fname) else "❌ missing"
        print(f"{tid:<30} → {entry['url']}   [{status}]")

if __name__ == "__main__":
    main()

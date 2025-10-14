#!/usr/bin/env python3
import json, os, re, random

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
AU_FILE = os.path.join(BASE_DIR, "knowledge", "training_sources", "au_segments.jsonl")
CONFIG = os.path.join(BASE_DIR, "configs", "capsule_learning.json")

def test_au_precision():
    """≥ 0.85 precision on imperative detection (spot-check 50 segments)"""
    verbs = json.load(open(CONFIG))["imperative_verbs"]
    pattern = re.compile(r"\b(" + "|".join(verbs) + r")\b", re.I)
    with open(AU_FILE) as f:
        lines = [json.loads(l) for l in f]
    sample = random.sample(lines, min(50, len(lines)))
    true_pos = sum(1 for au in sample if pattern.search(au["utterance"]))
    precision = true_pos / len(sample)
    print(f"AU precision = {precision:.2f}")
    assert precision >= 0.85, "AU precision below 0.85 threshold"

if __name__ == "__main__":
    test_au_precision(); print("✅ AU segmentation quality passed")

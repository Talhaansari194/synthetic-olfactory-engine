#!/bin/bash
set -e

echo "=== Building Capsules from Training Data ==="

# Use python3 explicitly (since macOS/Linux often don’t map `python` -> `python3`)
PYTHON="python3"

$PYTHON services/capsule_learning/yt_fetch_catalog.py
$PYTHON services/capsule_learning/transcribe_media.py
$PYTHON services/capsule_learning/segment_timelines.py
$PYTHON services/capsule_learning/extract_checklists.py
$PYTHON services/capsule_learning/derive_cognitive_graph.py
$PYTHON services/capsule_learning/compile_capsule_traits.py
$PYTHON services/capsule_learning/validate_capsule_traits.py
$PYTHON services/capsule_learning/knit_with_skillgraph.py

echo "✅ Build complete: check knowledge/compiled_capsules/"

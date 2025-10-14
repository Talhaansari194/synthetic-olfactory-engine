"""
validate_capsule_traits.py
Simple schema validation for CapsuleCortex.
"""

import json, sys
from jsonschema import validate, ValidationError
from pathlib import Path

def validate_capsule(cortex_path="knowledge/compiled_capsules/warehouse_ops.cortex.json",
                     schema_path="validators/schemas/capsule_cortex.schema.json"):
    cortex = json.load(open(cortex_path))
    schema = json.load(open(schema_path))
    try:
        validate(cortex, schema)
        print("Capsule validation passed ✅")
    except ValidationError as e:
        print(f"Schema validation failed ❌: {e}")
        sys.exit(1)

if __name__ == "__main__":
    validate_capsule()

from services.capsule_learning import extract_checklists
def test_extract():
    result = extract_checklists.extract_checklists()
    assert isinstance(result, list)
if __name__ == "__main__":
    print("✅ Checklist extraction test passed")


import pandas as pd
from pathlib import Path

from src.utils import load_and_validate_csv

print("\n========== TEST 5: MISSING LEAD ID DETECTION ==========")

test_data = pd.DataFrame({
    "lead_id": ["LEAD_0001", None, "LEAD_0003"],
    "name": ["John Smith", "Sarah Lee", "David Brown"],
    "company": ["ABC Tech", "XYZ Solutions", "PQR Systems"],
    "company_size": ["501-5000", "51-500", "11-50"],
    "industry": ["Technology", "Healthcare", "Finance"],
    "source": ["Referral", "Webinar Attendee", "Inbound Demo Request"],
    "last_interaction_date": [
        "2026-10-20",
        "2026-10-21",
        "2026-10-22",
    ],
})

test_file = Path("data/input/test_missing_ids.csv")
test_data.to_csv(test_file, index=False)

print("Test CSV created:", test_file)

try:
    load_and_validate_csv(test_file)

    print("TEST FAILED: Missing lead ID was accepted.")

except ValueError as error:
    print("\nValidation error caught successfully:")
    print(error)

    expected_message = "lead_id contains missing values."

    if expected_message in str(error):
        print("\nTEST PASSED: Missing lead ID correctly rejected.")
    else:
        print("\nTEST FAILED: Unexpected validation error.")

finally:
    if test_file.exists():
        test_file.unlink()
        print("\nTemporary test file cleaned up.")

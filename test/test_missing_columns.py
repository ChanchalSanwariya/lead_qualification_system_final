
import pandas as pd
from pathlib import Path

from src.utils import load_and_validate_csv

print("\n========== TEST 2: MISSING REQUIRED COLUMNS ==========")

# Create a temporary CSV with missing required columns.
test_data = pd.DataFrame({
    "name": ["John Smith", "Sarah Lee"],
    "company": ["ABC Technologies", "XYZ Solutions"],
    "industry": ["Technology", "Healthcare"],
    "source": ["Inbound Demo Request", "Referral"],
})

test_file = Path("data/input/test_missing_columns.csv")

test_data.to_csv(test_file, index=False)

print("Test CSV created:", test_file)

try:
    load_and_validate_csv(test_file)

    print("TEST FAILED: Missing columns were not detected.")

except ValueError as error:
    print("\nValidation error caught successfully:")
    print(error)

    expected_columns = [
        "company_size",
        "last_interaction_date",
    ]

    if all(column in str(error) for column in expected_columns):
        print("\nTEST PASSED: All missing columns detected.")
    else:
        print("\nTEST FAILED: Error message does not list expected columns.")

finally:
    if test_file.exists():
        test_file.unlink()
        print("\nTemporary test file cleaned up.")

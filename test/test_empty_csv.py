
import pandas as pd
from pathlib import Path

from src.utils import load_and_validate_csv, REQUIRED_COLUMNS

print("\n========== TEST 3: EMPTY CSV HANDLING ==========")

# Create a CSV with required headers but zero records.
empty_data = pd.DataFrame(columns=REQUIRED_COLUMNS)

test_file = Path("data/input/test_empty.csv")
empty_data.to_csv(test_file, index=False)

print("Empty CSV created:", test_file)

try:
    load_and_validate_csv(test_file)

    print("TEST FAILED: Empty CSV was accepted.")

except ValueError as error:
    print("\nValidation error caught successfully:")
    print(error)

    expected_message = "Uploaded CSV contains no lead records."

    if expected_message in str(error):
        print("\nTEST PASSED: Empty CSV correctly rejected.")
    else:
        print("\nTEST FAILED: Unexpected validation error.")

finally:
    if test_file.exists():
        test_file.unlink()
        print("\nTemporary test file cleaned up.")

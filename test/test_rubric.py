
from datetime import date

from src.utils import (
    PROJECT_ROOT,
    load_and_validate_csv,
)

from src.rubric import run_rubric


# Load the default dataset
input_file = (
    PROJECT_ROOT
    / "data"
    / "input"
    / "leads_full_scale_100.csv"
)

leads = load_and_validate_csv(input_file)

print("Total leads loaded:", len(leads))

# Run rule-based assessment
results = run_rubric(
    leads,
    evaluation_date=date.today()
)

print("\nRUBRIC RESULTS")
print("-" * 40)

print(
    "Total leads:",
    len(results)
)

print(
    "Ready for industry assessment:",
    (
        results["data_status"]
        == "ready_for_industry_assessment"
    ).sum()
)

print(
    "Needs review:",
    (
        results["data_status"]
        == "needs_review"
    ).sum()
)

print("\nSample results:")

print(
    results[
        [
            "lead_id",
            "name",
            "size_rating",
            "source_rating",
            "recency_rating",
            "data_status",
            "review_reasons",
        ]
    ].head(10).to_string(index=False)
)

# Save temporary test output
output_file = (
    PROJECT_ROOT
    / "outputs"
    / "rubric_test_output.csv"
)

results.to_csv(output_file, index=False)

print("\nOutput saved:", output_file)

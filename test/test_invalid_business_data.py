
import pandas as pd
from datetime import date

from src.rubric import run_rubric

print("\n========== TEST 7: INVALID BUSINESS DATA ==========")

evaluation_date = date(2026, 10, 31)

test_data = pd.DataFrame({
    "lead_id": [
        "LEAD_0001",
        "LEAD_0002",
        "LEAD_0003",
        "LEAD_0004",
    ],
    "name": [
        "John Smith",
        "Sarah Lee",
        "David Brown",
        "Emma Wilson",
    ],
    "company": [
        "ABC Tech",
        "XYZ Solutions",
        "PQR Systems",
        "LMN Software",
    ],
    "company_size": [
        "unknown",
        "501",
        "501",
        "501",
    ],
    "industry": [
        "Technology",
        "Healthcare",
        "Finance",
        "Technology",
    ],
    "source": [
        "Referral",
        "Referral",
        "Referral",
        "Unknown Source",
    ],
    "last_interaction_date": [
        "2026-10-20",
        "not-a-date",
        "2026-11-05",
        "2026-10-20",
    ],
})

results = run_rubric(
    test_data,
    evaluation_date=evaluation_date
)

print("\nTest results:")

for _, row in results.iterrows():
    print(f"\nLead ID: {row['lead_id']}")
    print("Size rating:", row["size_rating"])
    print("Source rating:", row["source_rating"])
    print("Recency rating:", row["recency_rating"])
    print("Data status:", row["data_status"])
    print("Review reasons:", row["review_reasons"])

# Verify expected behavior.
assert results["data_status"].eq("needs_review").all()

assert "Missing or invalid company size" in results.iloc[0]["review_reasons"]
assert "Missing, invalid or future interaction date" in results.iloc[1]["review_reasons"]
assert "Missing, invalid or future interaction date" in results.iloc[2]["review_reasons"]
assert "Missing or unrecognized source" in results.iloc[3]["review_reasons"]

print("\nTEST PASSED: All invalid business data correctly flagged for review.")

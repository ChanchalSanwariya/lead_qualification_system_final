
import pandas as pd

from src.outreach import generate_outreach

print("\n========== TEST 8: NO QUALIFIED LEADS ==========")

# Create scoring results with no qualified leads.
scoring_results = pd.DataFrame({
    "lead_id": ["LEAD_0001", "LEAD_0002", "LEAD_0003"],
    "name": ["John Smith", "Sarah Lee", "David Brown"],
    "company": ["ABC Tech", "XYZ Solutions", "PQR Systems"],
    "decision": ["review", "rejected", "review"],
})

print("Total leads:", len(scoring_results))
print(
    "Qualified leads:",
    (scoring_results["decision"] == "qualified").sum()
)

# Execute outreach generation.
results = generate_outreach(scoring_results)

print("\n========== TEST RESULTS ==========")

print("Returned records:", len(results))
print("Returned columns:", list(results.columns))

expected_columns = [
    "lead_id",
    "name",
    "company",
    "subject",
    "email_body",
    "generation_status",
]

assert results.empty
assert list(results.columns) == expected_columns

print("\nTEST PASSED: Outreach safely skipped.")
print("No qualified leads. No API client required.")


import pandas as pd
from pathlib import Path

print("\n========== TEST 10: OUTPUT INTEGRITY ==========")

# Use the second run from Test 1.
run_dir = Path(
    "outputs/pipeline_runs/20261031_213344_342122_3557ea"
)

assert run_dir.exists(), "Pipeline run directory not found."

# Required output files.
required_files = [
    "rubric_results.csv",
    "industry_results.csv",
    "scoring_results.csv",
    "outreach_results.csv",
    "run_summary.csv",
]

for filename in required_files:
    file_path = run_dir / filename

    assert file_path.exists(), f"Missing file: {filename}"

    print("File found:", filename)

# Load saved outputs.
rubric = pd.read_csv(run_dir / "rubric_results.csv")
industry = pd.read_csv(run_dir / "industry_results.csv")
scoring = pd.read_csv(run_dir / "scoring_results.csv")
outreach = pd.read_csv(run_dir / "outreach_results.csv")
summary = pd.read_csv(run_dir / "run_summary.csv")

print("\n========== RECORD COUNTS ==========")

print("Rubric records:", len(rubric))
print("Industry records:", len(industry))
print("Scoring records:", len(scoring))
print("Outreach records:", len(outreach))

# Verify pipeline record counts.
assert len(rubric) == 100
assert len(industry) == 100
assert len(scoring) == 100

# Verify unique lead IDs.
assert rubric["lead_id"].is_unique
assert industry["lead_id"].is_unique
assert scoring["lead_id"].is_unique

print("\nUnique lead ID checks: PASSED")

# Verify every scoring lead exists in rubric and industry.
rubric_ids = set(rubric["lead_id"].astype(str))
industry_ids = set(industry["lead_id"].astype(str))
scoring_ids = set(scoring["lead_id"].astype(str))

assert rubric_ids == industry_ids == scoring_ids

print("Cross-stage lead ID reconciliation: PASSED")

# Verify outreach contains only qualified leads.
qualified_ids = set(
    scoring.loc[
        scoring["decision"] == "qualified",
        "lead_id"
    ].astype(str)
)

outreach_ids = set(outreach["lead_id"].astype(str))

assert outreach_ids == qualified_ids
assert outreach["lead_id"].is_unique

print("Qualified-to-outreach reconciliation: PASSED")

# Verify outreach generation status.
assert outreach["generation_status"].eq("completed").all()

print("Outreach generation status: PASSED")

# Display summary.
print("\n========== SAVED RUN SUMMARY ==========")
print(summary.to_string(index=False))

print("\nTEST PASSED: All output integrity checks successful.")

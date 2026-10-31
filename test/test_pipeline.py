
from src.pipeline import run_pipeline


# ==========================================
# END-TO-END PIPELINE TEST
# ==========================================

print("\n========== STARTING PIPELINE TEST ==========")

input_path = "data/input/leads_full_scale_100.csv"

results = run_pipeline(input_path)


# ==========================================
# VALIDATE PIPELINE OUTPUTS
# ==========================================

print("\n========== PIPELINE VALIDATION ==========")

print("Run ID:", results["run_id"])
print("Output folder:", results["run_dir"])

print("\nRubric records:", len(results["rubric_results"]))
print("Industry records:", len(results["industry_results"]))
print("Scoring records:", len(results["scoring_results"]))
print("Outreach records:", len(results["outreach_results"]))

print("\nDecision counts:")
print(
    results["scoring_results"]["decision"]
    .value_counts()
    .to_string()
)

print("\nOutreach status:")
print(
    results["outreach_results"]["generation_status"]
    .value_counts(dropna=False)
    .to_string()
)

print("\n========== FILE VALIDATION ==========")

from pathlib import Path

run_dir = Path(results["run_dir"])

expected_files = [
    "rubric_results.csv",
    "industry_results.csv",
    "scoring_results.csv",
    "outreach_results.csv",
    "run_summary.csv",
]

for filename in expected_files:
    file_path = run_dir / filename
    print(
        filename,
        "->",
        "EXISTS" if file_path.exists() else "MISSING"
    )

print("\nEnd-to-end pipeline test completed!")

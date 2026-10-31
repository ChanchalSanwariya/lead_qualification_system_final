
import pandas as pd

scoring = pd.read_csv("outputs/scoring_test_output.csv")

industry_columns = [
    "lead_id",
    "industry_rating",
    "reasoning",
    "confidence",
    "needs_review",
    "assessment_status",
]

missing = [
    col for col in industry_columns
    if col not in scoring.columns
]

if missing:
    raise ValueError(f"Missing columns: {missing}")

industry_snapshot = scoring[industry_columns].copy()

output_path = "outputs/industry_scoring_run.csv"
industry_snapshot.to_csv(output_path, index=False)

print("Industry snapshot saved:", output_path)
print("Total records:", len(industry_snapshot))
print(
    "Needs review:",
    industry_snapshot["needs_review"].sum()
)
print(
    "Completed:",
    (industry_snapshot["assessment_status"] == "completed").sum()
)

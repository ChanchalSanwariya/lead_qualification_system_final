
import pandas as pd
from datetime import date

from src.utils import load_and_validate_csv
from src.rubric import run_rubric
from src.scoring import score_leads


# STEP 1: LOAD ORIGINAL DATA

print("\n========== STEP 1: DATA LOADING ==========")

leads = load_and_validate_csv(
    "data/input/leads_full_scale_100.csv"
)

print("Total leads:", len(leads))


# STEP 2: RUN RULE-BASED RUBRIC

print("\n========== STEP 2: RUBRIC ASSESSMENT ==========")

rubric_results = run_rubric(
    leads,
    evaluation_date=date.today()
)

print("Rubric assessment completed.")


# STEP 3: LOAD SAVED INDUSTRY RESULTS

print("\n========== STEP 3: INDUSTRY RESULTS ==========")

industry_results = pd.read_csv(
    "outputs/industry_scoring_run.csv"
)

print("Saved industry results:", len(industry_results))


# STEP 4: RUN WEIGHTED SCORING

print("\n========== STEP 4: FINAL SCORING ==========")

scoring_results = score_leads(
    rubric_results,
    industry_results
)

print("Scoring completed.")


# STEP 5: DECISION SUMMARY

print("\n========== DECISION SUMMARY ==========")

print(
    scoring_results["decision"]
    .value_counts()
    .reindex(
        ["qualified", "review", "rejected"],
        fill_value=0
    )
)

print(
    "\nAverage weighted score:",
    round(scoring_results["weighted_score"].mean(), 2)
)


# STEP 6: TOP QUALIFIED LEADS

print("\n========== TOP QUALIFIED LEADS ==========")

qualified = scoring_results[
    scoring_results["decision"] == "qualified"
].sort_values("priority_rank")

columns = [
    "priority_rank",
    "name",
    "company",
    "industry_rating",
    "weighted_score",
    "decision",
]

print(qualified[columns].head(10).to_string(index=False))


# STEP 7: DATA INTEGRITY

print("\n========== DATA INTEGRITY ==========")

print("Total records:", len(scoring_results))
print("Unique lead IDs:", scoring_results["lead_id"].nunique())
print("Duplicate lead IDs:", scoring_results["lead_id"].duplicated().sum())


# STEP 8: SAVE REPRODUCIBLE OUTPUT

output_path = "outputs/scoring_reproducible_output.csv"

scoring_results.to_csv(output_path, index=False)

print("\nSaved:", output_path)
print("\nReproducible scoring test completed!")

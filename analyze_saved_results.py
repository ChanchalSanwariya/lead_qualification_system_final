
import pandas as pd
from pathlib import Path


# ==========================================
# STEP 1: LOAD SAVED RESULTS
# ==========================================

industry_path = Path("outputs/industry_test_output.csv")
scoring_path = Path("outputs/scoring_test_output.csv")

if not industry_path.exists():
    raise FileNotFoundError(
        f"Industry results not found: {industry_path}"
    )

if not scoring_path.exists():
    raise FileNotFoundError(
        f"Scoring results not found: {scoring_path}"
    )

industry_results = pd.read_csv(industry_path)
scoring_results = pd.read_csv(scoring_path)

print("\n========== SAVED RESULTS LOADED ==========")
print("Industry records:", len(industry_results))
print("Scoring records:", len(scoring_results))


# ==========================================
# STEP 2: DECISION SUMMARY
# ==========================================

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


# ==========================================
# STEP 3: INDUSTRY REVIEW ANALYSIS
# ==========================================

print("\n========== INDUSTRY REVIEW ANALYSIS ==========")

print(
    industry_results["needs_review"]
    .value_counts(dropna=False)
)

print("\nAssessment status:")
print(
    industry_results["assessment_status"]
    .value_counts(dropna=False)
)


# ==========================================
# STEP 4: REVIEW REASON BREAKDOWN
# ==========================================

print("\n========== REVIEW REASON BREAKDOWN ==========")

industry_flagged = scoring_results[
    scoring_results["needs_review"].fillna(True)
]

score_based_review = scoring_results[
    (scoring_results["decision"] == "review")
    & (~scoring_results["needs_review"].fillna(True))
]

print(
    "Industry flagged for review:",
    len(industry_flagged)
)

print(
    "Review due to weighted score:",
    len(score_based_review)
)

print("\nIndustry flag vs final decision:")

print(
    pd.crosstab(
        scoring_results["decision"],
        scoring_results["needs_review"]
    )
)


# ==========================================
# STEP 5: TOP QUALIFIED LEADS
# ==========================================

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

print(
    qualified[columns]
    .head(10)
    .to_string(index=False)
)


# ==========================================
# STEP 6: SAVE REVIEW ANALYSIS
# ==========================================

review_analysis = scoring_results[
    scoring_results["decision"] == "review"
].copy()

review_analysis.to_csv(
    "outputs/review_analysis.csv",
    index=False
)

print("\nSaved: outputs/review_analysis.csv")


# ==========================================
# STEP 7: DATA INTEGRITY CHECK
# ==========================================

print("\n========== DATA INTEGRITY ==========")

print("Total leads:", len(scoring_results))

print(
    "Unique lead IDs:",
    scoring_results["lead_id"].nunique()
)

print(
    "Duplicate lead IDs:",
    scoring_results["lead_id"].duplicated().sum()
)

print("\nSaved-results analysis completed!")

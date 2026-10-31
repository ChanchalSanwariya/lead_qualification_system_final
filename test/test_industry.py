
from datetime import date

from src.utils import load_and_validate_csv
from src.rubric import run_rubric
from src.industry import assess_industries


input_path = "data/input/leads_full_scale_100.csv"

leads = load_and_validate_csv(input_path)

rubric_results = run_rubric(
    leads,
    evaluation_date=date.today()
)

industry_results = assess_industries(rubric_results)

print("\nIndustry assessment completed!")
print("Total results:", len(industry_results))
print(
    "Completed:",
    (industry_results["assessment_status"] == "completed").sum()
)
print(
    "Needs review:",
    industry_results["needs_review"].sum()
)

print("\nSample results:")
print(industry_results.head(10).to_string(index=False))

industry_results.to_csv(
    "outputs/industry_test_output.csv",
    index=False
)

print("\nSaved: outputs/industry_test_output.csv")

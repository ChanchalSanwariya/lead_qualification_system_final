
from datetime import date, datetime
from uuid import uuid4
from pathlib import Path

import pandas as pd

from src.utils import load_and_validate_csv
from src.rubric import run_rubric
from src.industry import assess_industries
from src.scoring import score_leads
from src.outreach import generate_outreach


def run_pipeline(
    input_path,
    evaluation_date=None,
    existing_industry_results_path=None,
    run_label=None,
    generate_outreach_messages=True,
    run_id=None,
    output_dir=None
):
    """
    Execute the complete lead intelligence pipeline.

    Flow:
    Load -> Rubric -> Industry -> Scoring -> Outreach
    """

    # Create a unique folder for every pipeline execution.
    if run_id is None:

        run_id = (
            datetime.now().strftime("%Y%m%d_%H%M%S_%f")
            + "_"
            + uuid4().hex[:6]
        )


    if output_dir is not None:

        run_dir = Path(output_dir)

    elif run_label:

        run_dir = (
            Path("outputs")
            / "pipeline_runs"
            / run_label
            / run_id
        )

    else:

        run_dir = (
            Path("outputs")
            / "pipeline_runs"
            / run_id
        )


    run_dir.mkdir(
        parents=True,
        exist_ok=True
    )
    print("\n====================================")
    print("LEAD INTELLIGENCE PIPELINE STARTED")
    print("Run ID:", run_id)
    print("====================================")

    # STEP 1: LOAD AND VALIDATE
    print("\n[1/5] Loading and validating leads...")

    leads = load_and_validate_csv(input_path)

    print("Leads loaded:", len(leads))

    # STEP 2: RULE-BASED RUBRIC
    print("\n[2/5] Running rule-based rubric...")

    if evaluation_date is None:
        evaluation_date = date.today()

    rubric_results = run_rubric(
        leads,
        evaluation_date=evaluation_date
    )

    rubric_results.to_csv(
        run_dir / "rubric_results.csv",
        index=False
    )

    print("Rubric assessment completed.")

    # STEP 3: INDUSTRY ASSESSMENT

    if existing_industry_results_path:

        print("\n[3/5] Reusing existing industry assessment...")

        industry_results = pd.read_csv(
            existing_industry_results_path
        )

    else:

        print("\n[3/5] Running NVIDIA industry assessment...")

        industry_results = assess_industries(rubric_results)

    industry_results.to_csv(
        run_dir / "industry_results.csv",
        index=False
    )

    print("Industry assessment completed.")

    industry_results.to_csv(
        run_dir / "industry_results.csv",
        index=False
    )

    print("Industry assessment completed.")

    # STEP 4: WEIGHTED SCORING
    print("\n[4/5] Calculating weighted scores...")

    scoring_results = score_leads(
        rubric_results,
        industry_results
    )

    scoring_results.to_csv(
        run_dir / "scoring_results.csv",
        index=False
    )

    print("Scoring completed.")

    # STEP 5: PERSONALIZED OUTREACH
    if generate_outreach_messages:
        print("\n[5/5] Generating personalized outreach...")
        outreach_results = generate_outreach(scoring_results)

    else:
        print("\n[5/5] Historical simulation: outreach skipped.")

        outreach_results = pd.DataFrame(
            columns=[
                "lead_id",
                "name",
                "company",
                "subject",
                "email_body",
                "generation_status"
            ]
        )

    outreach_results.to_csv(
        run_dir / "outreach_results.csv",
        index=False
    )

    print("Outreach step completed.")

    # FINAL SUMMARY
    decision_counts = (
        scoring_results["decision"]
        .value_counts()
        .reindex(
            ["qualified", "review", "rejected"],
            fill_value=0
        )
    )

    summary = pd.DataFrame({
        "metric": [
            "run_id",
            "total_leads",
            "qualified",
            "review",
            "rejected",
            "average_weighted_score",
            "outreach_generated",
            "outreach_failed",
        ],
        "value": [
            run_id,
            len(scoring_results),
            int(decision_counts["qualified"]),
            int(decision_counts["review"]),
            int(decision_counts["rejected"]),
            round(
                scoring_results["weighted_score"].mean(),
                2
            ),
            int(
                (outreach_results["generation_status"] == "completed").sum()
            ),
            int(
                (outreach_results["generation_status"] == "failed").sum()
            ),
        ]
    })

    summary.to_csv(
        run_dir / "run_summary.csv",
        index=False
    )

    print("\n====================================")
    print("PIPELINE EXECUTION COMPLETED")
    print("====================================")

    print("\nDecision summary:")
    print(decision_counts.to_string())

    print("\nAverage weighted score:",
          round(scoring_results["weighted_score"].mean(), 2))

    print("\nOutput directory:", run_dir)

    return {
        "run_id": run_id,
        "run_dir": str(run_dir),
        "rubric_results": rubric_results,
        "industry_results": industry_results,
        "scoring_results": scoring_results,
        "outreach_results": outreach_results,
        "summary": summary,
    }


import pandas as pd


WEIGHTS = {
    "size_rating": 0.30,
    "industry_rating": 0.25,
    "source_rating": 0.30,
    "recency_rating": 0.15,
}

QUALIFIED_THRESHOLD = 8.0
REVIEW_THRESHOLD = 5.0


def calculate_weighted_score(row):
    """Calculate weighted lead qualification score."""

    score = (
        row["size_rating"] * WEIGHTS["size_rating"]
        + row["industry_rating"] * WEIGHTS["industry_rating"]
        + row["source_rating"] * WEIGHTS["source_rating"]
        + row["recency_rating"] * WEIGHTS["recency_rating"]
    )

    return round(float(score), 2)


def generate_decision(row):
    """Determine qualification decision with review overrides."""

    # Critical data-quality issues override the score.
    if row["data_status"] != "ready_for_industry_assessment":
        return "review"

    # Missing or invalid industry assessment.
    if pd.isna(row["industry_rating"]):
        return "review"

    if row["assessment_status"] != "completed":
        return "review"

    # LLM uncertainty override.
    if bool(row["needs_review"]):
        return "review"

    score = row["weighted_score"]

    if score >= QUALIFIED_THRESHOLD:
        return "qualified"

    if score >= REVIEW_THRESHOLD:
        return "review"

    return "rejected"


def generate_reasoning(row):
    """Generate an explanation for the final decision."""

    reasons = []

    reasons.append(
        f"Company size rating: {row['size_rating']}/10"
    )

    reasons.append(
        f"Industry fit rating: {row['industry_rating']}/10"
    )

    reasons.append(
        f"Source intent rating: {row['source_rating']}/10"
    )

    reasons.append(
        f"Recency rating: {row['recency_rating']}/10"
    )

    if bool(row["needs_review"]):
        reasons.append(
            "Industry assessment requires manual review."
        )

    if row["data_status"] != "ready_for_industry_assessment":
        reasons.append(
            f"Data-quality issue: {row['review_reasons']}"
        )

    reasons.append(
        f"Final weighted score: {row['weighted_score']}/10"
    )

    return " | ".join(reasons)


def score_leads(rubric_results, industry_results):
    """Combine rubric and industry assessments."""

    # Prevent accidental duplicate records.
    if rubric_results["lead_id"].duplicated().any():
        raise ValueError("Duplicate lead IDs in rubric results.")

    if industry_results["lead_id"].duplicated().any():
        raise ValueError("Duplicate lead IDs in industry results.")

    # Merge assessments using lead_id.
    results = rubric_results.merge(
        industry_results,
        on="lead_id",
        how="left",
        validate="one_to_one",
    )

    # Check whether every lead has an industry result.
    missing_assessments = results["assessment_status"].isna()

    results.loc[
        missing_assessments,
        "needs_review"
    ] = True

    results.loc[
        missing_assessments,
        "assessment_status"
    ] = "missing"

    # Calculate weighted score only when all ratings exist.
    results["weighted_score"] = results.apply(
        lambda row: (
            calculate_weighted_score(row)
            if (
                pd.notna(row["size_rating"])
                and pd.notna(row["industry_rating"])
                and pd.notna(row["source_rating"])
                and pd.notna(row["recency_rating"])
            )
            else None
        ),
        axis=1,
    )

    # Determine final decision.
    results["decision"] = results.apply(
        generate_decision,
        axis=1,
    )

    # Generate decision explanation.
    results["decision_reasoning"] = results.apply(
        generate_reasoning,
        axis=1,
    )

    # Rank qualified leads by score.
    results["priority_rank"] = pd.NA

    qualified_mask = results["decision"] == "qualified"

    results.loc[
        qualified_mask,
        "priority_rank"
    ] = (
        results.loc[
            qualified_mask,
            "weighted_score"
        ]
        .rank(method="first", ascending=False)
        .astype(int)
    )

    results["priority_rank"] = results[
        "priority_rank"
    ].astype("Int64")

    # Sort qualified leads first, followed by review and rejected.
    decision_order = {
        "qualified": 0,
        "review": 1,
        "rejected": 2,
    }

    results["_decision_order"] = results[
        "decision"
    ].map(decision_order)

    results = results.sort_values(
        by=["_decision_order", "weighted_score"],
        ascending=[True, False],
        na_position="last",
    )

    results = results.drop(
        columns=["_decision_order"]
    ).reset_index(drop=True)

    return results

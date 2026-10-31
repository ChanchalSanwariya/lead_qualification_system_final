
from datetime import date
import pandas as pd


# --------------------------------------------------
# 1. COMPANY SIZE SCORING
# --------------------------------------------------

def calculate_size_rating(company_size):
    """
    Score company size from 1 to 10.
    """

    if pd.isna(company_size):
        return None

    try:
        size = float(company_size)
    except (ValueError, TypeError):
        return None

    if size <= 0:
        return None

    if 501 <= size <= 5000:
        return 10
    elif size > 5000:
        return 9
    elif 51 <= size <= 500:
        return 8
    elif 11 <= size <= 50:
        return 6
    else:
        return 4


# --------------------------------------------------
# 2. LEAD SOURCE SCORING
# --------------------------------------------------

SOURCE_SCORES = {
    "inbound demo request": 10,
    "sales call": 9,
    "referral": 8,
    "webinar attendee": 7,
    "content download": 5,
    "linkedin outreach": 4,
}


def calculate_source_rating(source):
    """
    Score lead source based on buying intent.
    """

    if pd.isna(source):
        return None

    normalized = str(source).strip().lower()

    return SOURCE_SCORES.get(normalized)


# --------------------------------------------------
# 3. RECENCY SCORING
# --------------------------------------------------

def calculate_recency_rating(
    interaction_date,
    evaluation_date
):
    """
    Calculate score using days since last interaction.
    """

    if pd.isna(interaction_date):
        return None

    try:
        interaction = pd.to_datetime(
            interaction_date,
            errors="raise"
        ).date()

    except (ValueError, TypeError):
        return None

    days = (evaluation_date - interaction).days

    if days < 0:
        return None
    elif days <= 7:
        return 10
    elif days <= 30:
        return 8
    elif days <= 90:
        return 5
    elif days <= 180:
        return 3
    else:
        return 1


# --------------------------------------------------
# 4. DATA QUALITY FLAGS
# --------------------------------------------------

def identify_review_reasons(row):
    """
    Identify missing or invalid information.
    """

    reasons = []

    # Name validation
    if pd.isna(row["name"]) or not str(row["name"]).strip():
        reasons.append("Missing name")

    # Company validation
    if pd.isna(row["company"]) or not str(row["company"]).strip():
        reasons.append("Missing company")

    # Industry validation
    if pd.isna(row["industry"]) or not str(row["industry"]).strip():
        reasons.append("Missing industry")

    # Company size validation
    if pd.isna(row["size_rating"]):
        reasons.append("Missing or invalid company size")

    # Source validation
    if pd.isna(row["source_rating"]):
        reasons.append("Missing or unrecognized source")

    # Date validation
    if pd.isna(row["recency_rating"]):
        reasons.append("Missing, invalid or future interaction date")

    return reasons


# --------------------------------------------------
# 5. MAIN RUBRIC PIPELINE
# --------------------------------------------------

def run_rubric(leads, evaluation_date=None):
    """
    Apply rule-based scoring and data quality checks.
    """

    if leads.empty:
        raise ValueError("No leads available for scoring.")

    if evaluation_date is None:
        evaluation_date = date.today()

    elif isinstance(evaluation_date, str):
        evaluation_date = pd.to_datetime(
            evaluation_date,
            errors="raise"
        ).date()

    elif isinstance(evaluation_date, pd.Timestamp):
        evaluation_date = evaluation_date.date()

    results = leads.copy()

    # Calculate individual ratings
    results["size_rating"] = results[
        "company_size"
    ].apply(calculate_size_rating)

    results["source_rating"] = results[
        "source"
    ].apply(calculate_source_rating)

    results["recency_rating"] = results[
        "last_interaction_date"
    ].apply(
        lambda value: calculate_recency_rating(
            value,
            evaluation_date
        )
    )

    # Identify records needing manual review
    results["review_reasons"] = results.apply(
        identify_review_reasons,
        axis=1
    )

    results["data_status"] = results[
        "review_reasons"
    ].apply(
        lambda reasons:
            "ready_for_industry_assessment"
            if not reasons
            else "needs_review"
    )

    # Convert reason lists into readable text
    results["review_reasons"] = results[
        "review_reasons"
    ].apply(
        lambda reasons: "; ".join(reasons)
    )

    return results

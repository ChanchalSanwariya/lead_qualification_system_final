
import pandas as pd

from src.outreach import generate_outreach


# ==========================================
# STEP 1: LOAD SAVED SCORING RESULTS
# ==========================================

print("\n========== STEP 1: LOAD SCORING RESULTS ==========")

scoring_path = "outputs/scoring_reproducible_output.csv"

scoring_results = pd.read_csv(scoring_path)

print("Total leads:", len(scoring_results))

qualified_count = (
    scoring_results["decision"] == "qualified"
).sum()

print("Qualified leads:", qualified_count)


# ==========================================
# STEP 2: GENERATE PERSONALIZED OUTREACH
# ==========================================

print("\n========== STEP 2: OUTREACH GENERATION ==========")

outreach_results = generate_outreach(scoring_results)


# ==========================================
# STEP 3: VALIDATE RESULTS
# ==========================================

print("\n========== STEP 3: VALIDATION ==========")

print("Total outreach records:", len(outreach_results))

if not outreach_results.empty:

    print(
        "Successfully generated:",
        (outreach_results["generation_status"] == "completed").sum()
    )

    print(
        "Failed:",
        (outreach_results["generation_status"] == "failed").sum()
    )

    print(
        "Duplicate lead IDs:",
        outreach_results["lead_id"].duplicated().sum()
    )

    print(
        "Empty subjects:",
        outreach_results["subject"].fillna("").eq("").sum()
    )

    print(
        "Empty email bodies:",
        outreach_results["email_body"].fillna("").eq("").sum()
    )


# ==========================================
# STEP 4: DISPLAY GENERATED EMAILS
# ==========================================

print("\n========== STEP 4: EMAIL PREVIEW ==========")

for _, row in outreach_results.head(3).iterrows():

    print("\n-----------------------------------")
    print("Name:", row["name"])
    print("Company:", row["company"])
    print("Subject:", row["subject"])
    print("\nEmail:")
    print(row["email_body"])


# ==========================================
# STEP 5: SAVE OUTREACH RESULTS
# ==========================================

print("\n========== STEP 5: SAVE RESULTS ==========")

output_path = "outputs/outreach_test_output.csv"

outreach_results.to_csv(
    output_path,
    index=False
)

print("Saved:", output_path)

print("\nOutreach testing completed!")

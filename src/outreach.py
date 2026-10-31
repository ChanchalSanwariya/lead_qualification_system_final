
import json
import time

import pandas as pd
from openai import OpenAI

from src.utils import get_config


# ==========================================
# STEP 1: CREATE NVIDIA CLIENT
# ==========================================

def create_client():
    config = get_config()

    if not config["nvidia_api_key"]:
        raise ValueError(
            "NVIDIA_API_KEY is missing. Check your .env file."
        )

    return OpenAI(
        base_url=config["base_url"],
        api_key=config["nvidia_api_key"],
    )


# ==========================================
# STEP 2: BUILD OUTREACH PROMPT
# ==========================================

def build_outreach_prompt(leads_batch):

    lead_details = []

    for lead in leads_batch:
        lead_details.append({
            "lead_id": lead["lead_id"],
            "name": lead["name"],
            "company": lead["company"],
            "industry": lead["industry"],
            "source": lead["source"],
        })

    return f"""
You are a professional B2B SaaS sales development representative.

Our company sells workflow automation software to mid-market businesses.

Generate one personalized FIRST-CONTACT sales email for each lead.

STRICT FACTUAL ACCURACY RULES:

1. Use only facts explicitly provided in the lead information
   or the business context.

2. You may discuss general workflow automation use cases
   relevant to the lead's industry.

3. Do not assume that a company has a specific problem,
   workflow, technology, customer base, or business process.

4. Do not invent company facts, statistics, achievements,
   customer references, integrations, or business challenges.

5. Do not claim that a lead requested a demo unless the
   source explicitly indicates "Inbound demo request".

6. Never claim that an action has already been completed
   unless the provided information explicitly confirms it.

7. NEVER claim or promise that:
   - A demo or walkthrough has been prepared.
   - A recording has been created or will be shared.
   - A proposal or report has been prepared.
   - A meeting has been scheduled.
   - A product assessment has been completed.
   - Any follow-up action has already been performed.

8. Do not promise future deliverables, meetings, recordings,
   reports, or other actions that the application cannot perform.

9. Use a low-pressure CTA that asks whether the recipient
   would be interested in learning more.

10. Address the lead using their first name.

11. Consider the lead source when choosing the email tone.
    Do not misrepresent the source as a confirmed conversation
    or purchase intention.

12. Keep the email professional, natural, concise,
    and relevant to the recipient.

13. Avoid exaggerated marketing language and unsupported
    performance claims.

14. Return exactly one email per lead.
    Preserve every lead_id exactly as provided.

15. If the available information is insufficient for strong
    personalization, use a modest industry-level observation
    rather than inventing details.

Return valid JSON in this structure:

{{
  "outreach": [
    {{
      "lead_id": "LEAD_0001",
      "subject": "Email subject",
      "email_body": "Complete email body"
    }}
  ]
}}

Lead information:
{json.dumps(lead_details, ensure_ascii=False)}
"""



# ==========================================
# STEP 3: GENERATE ONE BATCH
# ==========================================

def generate_outreach_batch(client, leads_batch):

    config = get_config()

    prompt = build_outreach_prompt(leads_batch)

    response = client.chat.completions.create(
        model=config["model"],
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a factual and conservative B2B email writer. "
                    "Never invent facts, claim completed actions, or promise "
                    "deliverables that are not explicitly authorized. "
                    "Follow the provided instructions and JSON schema exactly."
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0,
        response_format={"type": "json_object"},
        extra_body={
            "chat_template_kwargs": {
                "enable_thinking": False
            }
        },
    )

    content = response.choices[0].message.content

    if not content:
        raise ValueError("NVIDIA returned an empty response.")

    parsed = json.loads(content)

    if "outreach" not in parsed:
        raise ValueError("Missing 'outreach' key in model response.")

    generated = parsed["outreach"]

    # Check duplicate lead IDs returned by NVIDIA
    returned_ids = [
        str(item.get("lead_id", "")).strip()
        for item in generated
    ]

    if len(returned_ids) != len(set(returned_ids)):
        raise ValueError(
            "Duplicate lead IDs returned by NVIDIA."
        )

    expected_ids = {
        str(lead["lead_id"]) for lead in leads_batch
    }

    results = {}

    for item in generated:

        lead_id = str(item.get("lead_id", "")).strip()
        subject = str(item.get("subject", "")).strip()
        email_body = str(item.get("email_body", "")).strip()

        if lead_id not in expected_ids:
            continue

        if not subject or not email_body:
            continue

        results[lead_id] = {
            "lead_id": lead_id,
            "subject": subject,
            "email_body": email_body,
            "generation_status": "completed",
        }

    if set(results.keys()) != expected_ids:
        missing_ids = expected_ids - set(results.keys())

        raise ValueError(
            f"Missing or invalid outreach for leads: {missing_ids}"
        )

    return list(results.values())


# ==========================================
# STEP 4: GENERATE OUTREACH FOR QUALIFIED LEADS
# ==========================================

def generate_outreach(scoring_results):

    config = get_config()

    qualified = scoring_results[
        scoring_results["decision"] == "qualified"
    ].copy()

    qualified = qualified.reset_index(drop=True)

    if qualified.empty:
        print("No qualified leads found. Outreach skipped.")
        return pd.DataFrame(
            columns=[
                "lead_id",
                "name",
                "company",
                "subject",
                "email_body",
                "generation_status",
            ]
        )

    client = create_client()

    batch_size = config["outreach_batch_size"]
    max_retries = config["max_retries"]

    all_results = []

    total_batches = (
        len(qualified) + batch_size - 1
    ) // batch_size

    print("\n========== OUTREACH GENERATION ==========")
    print("Qualified leads:", len(qualified))
    print("Batch size:", batch_size)
    print("Total batches:", total_batches)

    for start in range(0, len(qualified), batch_size):

        batch = qualified.iloc[
            start:start + batch_size
        ]

        leads_batch = batch.to_dict("records")

        batch_number = start // batch_size + 1

        print(
            f"\nProcessing batch {batch_number}/{total_batches}"
        )

        generated = None

        for attempt in range(max_retries):

            try:
                generated = generate_outreach_batch(
                    client,
                    leads_batch,
                )

                print("Batch completed successfully.")
                break

            except Exception as error:

                print(
                    f"Attempt {attempt + 1}/{max_retries} failed: "
                    f"{error}"
                )

                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    print(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)

        if generated is None:

            print(
                f"Batch {batch_number} failed after all retries."
            )

            for lead in leads_batch:
                generated_item = {
                    "lead_id": str(lead["lead_id"]),
                    "subject": "",
                    "email_body": "",
                    "generation_status": "failed",
                }

                all_results.append(generated_item)

        else:
            all_results.extend(generated)

    outreach_results = pd.DataFrame(all_results)

    # Add lead details to generated outreach.
    lead_details = qualified[
        ["lead_id", "name", "company"]
    ].copy()

    lead_details["lead_id"] = (
        lead_details["lead_id"].astype(str)
    )

    outreach_results["lead_id"] = (
        outreach_results["lead_id"].astype(str)
    )

    outreach_results = lead_details.merge(
        outreach_results,
        on="lead_id",
        how="left",
        validate="one_to_one",
    )

    print("\n========== OUTREACH SUMMARY ==========")
    print("Total qualified leads:", len(qualified))
    print(
        "Successfully generated:",
        (outreach_results["generation_status"] == "completed").sum()
    )
    print(
        "Failed:",
        (outreach_results["generation_status"] == "failed").sum()
    )

    return outreach_results

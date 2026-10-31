
import json
import re
import time

import pandas as pd
from openai import OpenAI

from src.utils import get_config


SYSTEM_PROMPT = """
You are an industry-fit analyst for a B2B SaaS company.

The company sells workflow automation software.

Evaluate how well each lead's industry could benefit from workflow
automation software.

Scoring rubric:
10 = Strong fit with specific, clear automation use cases.
7  = Plausible industry use cases for workflow automation.
5  = Unclear, mixed, or insufficient industry evidence.
3  = Limited fit with few obvious use cases.

Important rules:
- Be conservative. Do not assume facts not provided.
- Do not invent company operations, tools, customers, or problems.
- If industry information is missing or unclear, use rating 5.
- Set needs_review=true when evidence is insufficient.
- Give a short explanation for every lead.
- Return valid JSON only.
"""


def create_client(config):
    """Create NVIDIA-compatible OpenAI client."""

    return OpenAI(
        base_url=config["base_url"],
        api_key=config["nvidia_api_key"],
        timeout=90.0,
    )


def extract_json(content):
    """Extract JSON object from model response."""

    content = content.strip()

    # Remove optional Markdown code fences.
    content = re.sub(r"^```(?:json)?\s*", "", content)
    content = re.sub(r"\s*```$", "", content)

    return json.loads(content)


def assess_batch(client, batch, config):
    """Assess one batch of leads."""

    leads_payload = []

    for _, row in batch.iterrows():
        leads_payload.append({
            "lead_id": row["lead_id"],
            "company": row["company"],
            "industry": row["industry"],
        })

    prompt = f"""
Assess the industry fit of these leads.

Return exactly this JSON structure:

{{
  "assessments": [
    {{
      "lead_id": "LEAD_0001",
      "industry_rating": 7,
      "reasoning": "Short evidence-based explanation.",
      "confidence": "high",
      "needs_review": false
    }}
  ]
}}

Rules:
- Include every supplied lead exactly once.
- Preserve each lead_id exactly.
- industry_rating must be 3, 5, 7, or 10.
- confidence must be high, medium, or low.
- Return JSON only.

Leads:
{json.dumps(leads_payload, ensure_ascii=False)}
"""

    max_retries = config["max_retries"]

    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=config["model"],
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
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

            result = extract_json(content)
            assessments = result.get("assessments")

            if not isinstance(assessments, list):
                raise ValueError("Response does not contain an assessments list.")

            expected_ids = set(batch["lead_id"].astype(str))
            returned_ids = [
                str(item.get("lead_id", ""))
                for item in assessments
            ]

            if len(returned_ids) != len(set(returned_ids)):
                raise ValueError("Duplicate lead IDs in model response.")

            if set(returned_ids) != expected_ids:
                raise ValueError("Missing or unexpected lead IDs in response.")

            validated = []

            for item in assessments:
                rating = int(item["industry_rating"])

                if rating not in (3, 5, 7, 10):
                    raise ValueError(
                        f"Invalid industry rating: {rating}"
                    )

                confidence = str(
                    item.get("confidence", "low")
                ).lower()

                if confidence not in ("high", "medium", "low"):
                    confidence = "low"

                reasoning = str(item.get("reasoning", "")).strip()

                if not reasoning:
                    reasoning = "Insufficient explanation from model."
                
                validated.append({
                    "lead_id": str(item["lead_id"]),
                    "industry_rating": rating,
                    "reasoning": reasoning,
                    "confidence": confidence,
                    "needs_review": (
                        bool(item.get("needs_review", False))
                        or confidence == "low"
                    ),
                    "assessment_status": "completed",
                })

            return validated

        except Exception as error:
            print(
                f"Batch attempt {attempt + 1}/{max_retries} failed: {error}"
            )

            if attempt == max_retries - 1:
                raise

            time.sleep(2 ** attempt)


def assess_industries(leads):
    """Assess all eligible leads in batches."""

    config = get_config()

    if not config["nvidia_api_key"]:
        raise ValueError(
            "NVIDIA_API_KEY is missing. Check your .env file."
        )

    batch_size = config["industry_batch_size"]

    client = create_client(config)

    eligible = leads[
        leads["data_status"] == "ready_for_industry_assessment"
    ].copy()

    skipped = leads[
        leads["data_status"] != "ready_for_industry_assessment"
    ].copy()

    all_results = []

    total_batches = (
        (len(eligible) + batch_size - 1) // batch_size
    )

    for batch_number, start in enumerate(
        range(0, len(eligible), batch_size),
        start=1
    ):
        batch = eligible.iloc[start:start + batch_size]

        print(
            f"Assessing batch {batch_number}/{total_batches} "
            f"({len(batch)} leads)"
        )

        try:
            results = assess_batch(client, batch, config)
            all_results.extend(results)

        except Exception as error:
            print(f"Batch failed permanently: {error}")

            for lead_id in batch["lead_id"]:
                all_results.append({
                    "lead_id": str(lead_id),
                    "industry_rating": None,
                    "reasoning": f"API assessment failed: {error}",
                    "confidence": "low",
                    "needs_review": True,
                    "assessment_status": "failed",
                })

    # Leads rejected from assessment due to data quality
    # remain in the output with a review flag.
    for _, row in skipped.iterrows():
        all_results.append({
            "lead_id": str(row["lead_id"]),
            "industry_rating": None,
            "reasoning": "Skipped due to data-quality issues.",
            "confidence": "low",
            "needs_review": True,
            "assessment_status": "skipped",
        })

    results_df = pd.DataFrame(all_results)

    # Preserve original lead order.
    results_df = leads[["lead_id"]].merge(
        results_df,
        on="lead_id",
        how="left",
        validate="one_to_one",
    )

    return results_df

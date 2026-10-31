# 04 — Industry Fit Assessment

## 1. Objective

The objective of industry fit assessment is to evaluate how well each lead's industry could benefit from the company's B2B workflow automation software.

The assessment uses NVIDIA's Nemotron model to analyze industry context and generate:

- Industry-fit rating
- Supporting reasoning
- Confidence level
- Review flag
- Assessment status

This LLM-based assessment contributes 25% to the final lead qualification score.

## 2. Model Configuration

| Configuration   | Value                                   |
| --------------- | --------------------------------------- |
| Provider        | NVIDIA                                  |
| Model           | `nvidia/nemotron-3.5-lightning-30b-a3b` |
| API interface   | OpenAI-compatible API                   |
| Temperature     | 0                                       |
| Response format | JSON object                             |
| Thinking mode   | Disabled                                |
| Batch size      | 25 leads                                |
| Maximum retries | 3                                       |

The API configuration is loaded from environment variables using the `.env` file.

API credentials are not hardcoded in the source code.

## 3. Industry Fit Rubric

The model evaluates the potential relevance of workflow automation to the lead's industry.

| Rating | Interpretation                                |
| ------ | --------------------------------------------- |
| 10     | Strong fit with specific automation use cases |
| 7      | Plausible industry use cases                  |
| 5      | Unclear, mixed, or insufficient evidence      |
| 3      | Limited fit                                   |

The model is instructed to provide conservative assessments and avoid inventing company operations, tools, customers, or business problems.

## 4. Processing Approach

The industry assessment module follows a batch-processing approach:

1. Receive leads eligible for industry assessment.
2. Divide eligible leads into batches.
3. Send company and industry information to NVIDIA.
4. Receive structured JSON assessments.
5. Validate returned lead IDs and industry ratings.
6. Capture reasoning, confidence, and `needs_review`.
7. Retry temporary API failures using configured retry logic.
8. Preserve skipped or failed leads with explicit assessment status information.

Batch processing reduces the number of individual API requests and makes the assessment process more efficient.

## 5. Response Validation and Error Handling

The module validates model responses before accepting assessment results.

Important validation checks include:

- Valid JSON response structure.
- Expected lead IDs are present.
- Industry ratings follow the supported rubric.
- Required assessment fields are available.
- Results are associated with the correct lead IDs.

Temporary failures are retried up to the configured maximum retry count.

The module also preserves skipped or unsuccessful assessments instead of silently dropping leads.

The `assessment_status` field helps distinguish completed assessments from skipped or failed assessments.

## 6. Review Flag Handling

The model returns a `needs_review` indicator alongside its industry assessment.

This flag identifies leads whose industry fit requires additional attention.

A completed assessment does not necessarily mean that the lead has a strong industry fit.

The final scoring module considers both the industry rating and review flag when determining the qualification decision.

## 7. Experiment 01 — Full-scale Dataset

**Input:** `leads_full_scale_100.csv`

| Metric                | Actual Result |
| --------------------- | ------------: |
| Total leads           |           100 |
| Batches processed     |             4 |
| Batch size            |            25 |
| Completed assessments |           100 |
| Needs review          |            24 |
| Assessment failures   |             0 |

## 8. Experiment Observations

- All 100 leads received completed assessments.
- The dataset was processed in four batches of 25 leads each.
- 24 leads were marked as requiring review by the model.
- No assessment failures were recorded in this experiment.
- A completed API response does not automatically indicate a strong industry fit.
- The review flag is considered during final lead qualification.

## 9. Output Artifacts

The integrated pipeline saves industry assessment results as:

`industry_results.csv`

The file is stored inside the corresponding pipeline run directory:

`outputs/pipeline_runs/<run_id>/industry_results.csv`

The results contain the following fields:

| Column              | Description                                 |
| ------------------- | ------------------------------------------- |
| `lead_id`           | Unique identifier for the lead              |
| `industry_rating`   | Industry-fit rating                         |
| `reasoning`         | Explanation supporting the rating           |
| `confidence`        | Model confidence                            |
| `needs_review`      | Indicates whether manual review is required |
| `assessment_status` | Status of the assessment                    |

## 10. Current Status

The industry assessment module and the first full-scale experiment have been completed successfully.

The module is designed to integrate LLM-based industry assessment with deterministic scoring dimensions such as company size, lead source intent, and interaction recency.

The resulting industry ratings are passed to the lead scoring module for final qualification.

# 08 — Testing and Experiments

## 1. Objective

The objective of reliability testing was to verify that the Lead Intelligence Studio handles repeated executions, invalid input data, missing information, API failures, and output consistency safely.

A total of 10 reliability experiments were performed. An additional historical simulation experiment was conducted to understand the impact of evaluation dates on lead qualification results.

## 2. Reliability Test Results Summary

| Test | Experiment                           | Result |
| ---- | ------------------------------------ | ------ |
| 1    | Idempotency and run isolation        | PASS   |
| 2    | Missing required columns             | PASS   |
| 3    | Empty CSV handling                   | PASS   |
| 4    | Duplicate lead ID detection          | PASS   |
| 5    | Missing lead ID detection            | PASS   |
| 6    | Blank lead ID detection              | PASS   |
| 7    | Invalid business data handling       | PASS   |
| 8    | No qualified leads / outreach safety | PASS   |
| 9    | API retry mechanism                  | PASS   |
| 10   | Output integrity and reconciliation  | PASS   |

**Overall: 10/10 reliability tests passed.**

## 3. Detailed Reliability Experiments

### 3.1 Test 1: Idempotency and Run Isolation

**Objective:** Verify that repeated pipeline executions create separate output directories without overwriting earlier results.

Input: `leads_full_scale_100.csv`

Two executions were performed.

| Metric             | Run 1 | Run 2 |
| ------------------ | ----: | ----: |
| Total leads        |   100 |   100 |
| Qualified          |     5 |     5 |
| Review             |    92 |    90 |
| Rejected           |     3 |     5 |
| Average score      |  6.43 |  6.47 |
| Separate directory |   Yes |   Yes |

Both executions generated unique run IDs and preserved their output files.

**Result: PASS**

Note: LLM-generated industry assessments can vary between independent executions. Therefore, identical scores are not guaranteed. This experiment verified run isolation and output preservation, not deterministic LLM results.

### 3.2 Test 2: Missing Required Columns

**Objective:** Verify that CSV files missing mandatory columns are rejected.

Test CSV omitted:

- `company_size`
- `last_interaction_date`

Observed validation error:

`Missing required columns: ['company_size', 'last_interaction_date']`

**Result: PASS**

### 3.3 Test 3: Empty CSV Handling

**Objective:** Verify that a CSV containing headers but no lead records is rejected.

Observed validation error:

`Uploaded CSV contains no lead records.`

**Result: PASS**

### 3.4 Test 4: Duplicate Lead ID Detection

**Objective:** Verify that duplicate lead IDs are rejected.

The test CSV contained `LEAD_0001` twice.

Observed validation error:

`Duplicate lead_id values found.`

**Result: PASS**

### 3.5 Test 5: Missing Lead ID Detection

**Objective:** Verify that missing lead IDs are rejected.

The test CSV contained a missing lead ID.

Observed validation error:

`lead_id contains missing values.`

**Result: PASS**

### 3.6 Test 6: Blank Lead ID Detection

**Objective:** Verify that whitespace-only lead IDs are rejected.

The test CSV contained a lead ID with whitespace characters.

Observed validation error:

`lead_id contains empty values.`

**Result: PASS**

### 3.7 Test 7: Invalid Business Data Handling

**Objective:** Verify that invalid business information is flagged for manual review.

Four scenarios were tested:

| Lead      | Invalid value            | Expected handling | Observed     |
| --------- | ------------------------ | ----------------- | ------------ |
| LEAD_0001 | Invalid company size     | needs_review      | needs_review |
| LEAD_0002 | Invalid interaction date | needs_review      | needs_review |
| LEAD_0003 | Future interaction date  | needs_review      | needs_review |
| LEAD_0004 | Unrecognized source      | needs_review      | needs_review |

The rubric correctly identified the corresponding review reasons.

**Result: PASS**

### 3.8 Test 8: No Qualified Leads — Outreach Safety

**Objective:** Verify that outreach generation safely handles a scenario with zero qualified leads.

Input:

- Total leads: 3
- Qualified: 0
- Review: 2
- Rejected: 1

Observed:

- Outreach generation skipped.
- Empty DataFrame returned.
- Expected output columns preserved.
- No NVIDIA client or API request required.

**Result: PASS**

### 3.9 Test 9: API Retry Mechanism

**Objective:** Verify that temporary API failures are handled using retries and exponential backoff.

A mocked API response simulated:

1. First attempt: temporary API failure.
2. Second attempt: rate-limit error.
3. Third attempt: successful response.

Observed:

- Total attempts: 3
- Retry waits: 1 second and 2 seconds.
- Successful outreach records: 1
- Failed records: 0
- Retry sleep calls: 2

No real NVIDIA API request was made during this test.

**Result: PASS**

### 3.10 Test 10: Output Integrity and Reconciliation

**Objective:** Verify that all pipeline output files exist and that records remain consistent across pipeline stages.

Run ID: `20261031_213344_342122_3557ea`

Required files verified:

- `rubric_results.csv`
- `industry_results.csv`
- `scoring_results.csv`
- `outreach_results.csv`
- `run_summary.csv`

Observed record counts:

| Output   | Records |
| -------- | ------: |
| Rubric   |     100 |
| Industry |     100 |
| Scoring  |     100 |
| Outreach |       5 |

Additional validations:

- Unique lead IDs in all three 100-record stages.
- Rubric, industry and scoring lead IDs matched exactly.
- Outreach lead IDs matched the qualified lead IDs.
- All five outreach records had `completed` status.
- No failed outreach records.

Saved run summary:

| Metric                 | Value |
| ---------------------- | ----: |
| Total leads            |   100 |
| Qualified              |     5 |
| Review                 |    90 |
| Rejected               |     5 |
| Average weighted score |  6.47 |
| Outreach generated     |     5 |
| Outreach failed        |     0 |

**Result: PASS**

## 4. Historical Simulation Experiment

### 4.1 Objective

Evaluate how the evaluation date affects lead recency ratings, weighted scores, and qualification decisions.

### 4.2 Experiment Configuration

- Dataset: `leads_full_scale_100.csv`
- Total leads: 100
- Historical evaluation date: 2024-01-21
- Existing industry assessments reused.
- Outreach generation skipped.
- Results stored in a separate `historical_simulation` directory.

The historical experiment reused previously generated NVIDIA industry assessments to avoid unnecessary API calls and isolate the impact of the evaluation date.

### 4.3 Results Comparison

| Metric             | Current Date Run | Historical Run |
| ------------------ | ---------------: | -------------: |
| Evaluation date    |       2026-10-31 |     2024-01-21 |
| Qualified          |                5 |             35 |
| Review             |               90 |             65 |
| Rejected           |                5 |              0 |
| Average Score      |             6.47 |           7.41 |
| Outreach Generated |                5 |              0 |

### 4.4 Observation

The dataset contains interaction dates between 2023-08-30 and 2024-01-20.

When evaluated on 2026-10-31, all leads received a recency rating of 1 because their interactions were old.

When evaluated on 2024-01-21, recency ratings reflected the actual age of each interaction.

This increased the average weighted score from 6.47 to 7.41 and qualified leads from 5 to 35.

The historical simulation demonstrated that the evaluation date is an important input to the lead scoring system.

### 4.5 Conclusion

Historical simulations should use a date appropriate to the dataset's time period, while production runs should use the actual business evaluation date.

Historical simulation was performed without regenerating industry assessments or outreach messages.

## 5. Overall Findings

All 10 reliability experiments passed.

The testing demonstrated that:

1. Repeated executions create independent run directories.
2. Invalid CSV structures are rejected with clear errors.
3. Missing, blank and duplicate lead IDs are detected.
4. Invalid business data is flagged for manual review.
5. Outreach generation safely skips when no leads qualify.
6. API retry logic recovers from simulated temporary failures.
7. Pipeline outputs maintain lead-level consistency across stages.
8. Generated outreach records correspond to qualified leads.
9. Evaluation dates have a measurable impact on recency ratings and qualification decisions.
10. Historical simulation can reuse existing industry assessments without additional NVIDIA API calls.

## 6. Testing Limitations

- NVIDIA API response variability means independent LLM runs may produce different assessments and scores.
- Retry behavior was tested using mocked failures rather than a real production outage.
- These experiments do not establish production-scale performance or concurrency behavior.
- The tests cover the implemented validation and pipeline scenarios, not every possible malformed CSV or API failure.
- Historical simulation results depend on the selected evaluation date and the quality of the original dataset.

## 7. Final Conclusion

The Lead Intelligence Studio successfully passed all 10 implemented reliability experiments.

The pipeline demonstrates reliable run isolation, input validation, business-rule review handling, retry recovery, and output integrity for the tested scenarios.

The additional historical simulation confirmed that evaluation-date selection significantly influences recency scoring and final lead qualification outcomes.

Together, these experiments provide evidence of the pipeline's reliability for the tested scenarios and complete the reliability testing phase of the project.

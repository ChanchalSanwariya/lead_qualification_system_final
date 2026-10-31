# 05 — Lead Scoring and Qualification

## 1. Objective

The objective of this module is to combine rule-based lead attributes and AI-based industry-fit assessment into a single weighted score.

Each lead receives:

- A weighted score out of 10
- A qualification decision
- A human-readable scoring explanation
- A priority rank for qualified leads

The scoring module combines deterministic business rules with LLM-generated industry assessments.

## 2. Weighted Scoring Model

The scoring model uses four components:

| Component           |   Weight | Assessment Method |
| ------------------- | -------: | ----------------- |
| Company size        |      30% | Rule-based        |
| Industry fit        |      25% | NVIDIA LLM        |
| Source intent       |      30% | Rule-based        |
| Interaction recency |      15% | Rule-based        |
| **Total**           | **100%** |                   |

### Formula

`Weighted Score = (Size × 0.30) + (Industry × 0.25) + (Source × 0.30) + (Recency × 0.15)`

All component ratings are measured on a scale of 1–10.

The weighted score is calculated only when all required component ratings are available.

## 3. Qualification Rules

| Weighted Score | Decision  |
| -------------- | --------- |
| 8.00–10.00     | Qualified |
| 5.00–7.99      | Review    |
| Below 5.00     | Rejected  |

Critical missing or invalid data and industry assessments marked `needs_review` override the score-based decision and send the lead to manual review.

Other review conditions include incomplete or unsuccessful industry assessments.

This ensures that uncertain records are not automatically qualified or rejected.

## 4. Implementation

The scoring logic is implemented in:

`src/scoring.py`

The main function is:

`score_leads(rubric_results, industry_results)`

The function:

1. Combines rule-based rubric results with industry assessment results.
2. Calculates weighted scores.
3. Assigns qualification decisions.
4. Generates human-readable reasoning.
5. Applies review overrides.
6. Ranks qualified leads in descending order of their scores.

The industry assessment and scoring stages are kept separate to support independent testing and reuse of saved assessment results.

## 5. Testing and Reproducibility

The scoring logic was tested using the 100-lead dataset.

An earlier scoring experiment used a saved NVIDIA industry assessment snapshot to avoid unnecessary API calls during repeated scoring tests.

The saved assessment snapshot was:

`outputs/industry_scoring_run.csv`

The reproducible test script was:

`test_scoring.py`

The experiment output was:

`outputs/scoring_reproducible_output.csv`

Reusing a saved industry assessment allows scoring logic to be tested independently of new LLM API responses.

However, reproducibility also depends on using the same evaluation date for interaction recency.

## 6. Experiment 01 — Earlier Reproducible Scoring Test

| Metric                 | Observed Result |
| ---------------------- | --------------: |
| Total leads            |             100 |
| Qualified              |               5 |
| Review                 |              93 |
| Rejected               |               2 |
| Average weighted score |            6.42 |
| Unique lead IDs        |             100 |
| Duplicate lead IDs     |               0 |

### Top Qualified Leads

| Rank | Lead            | Company                | Industry Rating | Weighted Score |
| ---: | --------------- | ---------------------- | --------------: | -------------: |
|    1 | Frank Liu       | Healthcare Systems Ltd |              10 |           8.35 |
|    2 | Karen Miller    | InsurancePro           |              10 |           8.35 |
|    3 | Derek Johnson   | Cloud Infrastructure   |              10 |           8.05 |
|    4 | Dominic Wheeler | Payment Processing     |              10 |           8.05 |
|    5 | Ulysses Morgan  | Autonomous Vehicles    |              10 |           8.05 |

These results represent the earlier saved-assessment scoring experiment and should not be interpreted as the output of every subsequent pipeline run.

## 7. Latest Integrated Pipeline Observation

A later integrated pipeline execution processed the same 100-lead dataset.

| Metric                 | Latest Observed Result |
| ---------------------- | ---------------------: |
| Total leads            |                    100 |
| Qualified              |                      5 |
| Review                 |                     90 |
| Rejected               |                      5 |
| Average weighted score |                   6.47 |

The results differ from the earlier scoring experiment because pipeline executions can use different LLM assessment outputs and evaluation dates.

The integrated pipeline stores its results in run-specific directories under:

`outputs/pipeline_runs/<run_id>/`

Relevant output files include:

- `rubric_results.csv`
- `industry_results.csv`
- `scoring_results.csv`
- `run_summary.csv`

## 8. Observations

- Only five leads crossed the qualification threshold in both observed experiments.
- Most leads fell into the review category, indicating a conservative qualification approach.
- No duplicate lead IDs were found in the earlier reproducible scoring experiment.
- Saved industry assessments reduce unnecessary API calls during repeated scoring tests.
- Changes in evaluation date affect interaction recency ratings.
- LLM assessment variation can also influence final qualification outcomes.

## 9. Engineering Decisions

Industry assessment and weighted scoring are maintained as separate stages.

This separation:

1. Avoids repeated NVIDIA API calls during scoring experiments.
2. Makes scoring tests easier to reproduce.
3. Allows scoring logic to be tested independently of the LLM.
4. Preserves the industry assessment used for a particular scoring run.
5. Improves modularity and maintainability.

For strict historical reproducibility, the evaluation date and industry assessment snapshot should both be preserved for each experiment.

## 10. Conclusion

The scoring module combines deterministic business rules with AI-based industry assessment to produce explainable lead qualification decisions.

The weighted scoring model provides a consistent framework for prioritizing leads, while review overrides prevent uncertain or incomplete records from being automatically processed.

Separating industry assessment from scoring also improves testing, reproducibility, and pipeline maintainability.

# 07 — End-to-End Pipeline Integration

## 1. Objective

The objective of this stage is to integrate all previously developed modules into one executable lead intelligence pipeline.

The integrated pipeline processes input leads from initial data loading through qualification and personalized outreach generation.

## 2. Pipeline Architecture

The execution flow is:

1. Load and validate input CSV.
2. Apply rule-based rubric.
3. Perform NVIDIA LLM industry-fit assessment.
4. Calculate weighted scores and qualification decisions.
5. Generate personalized outreach for qualified leads.
6. Save outputs and execution summary.

## 3. Implementation

Main pipeline module:

`src/pipeline.py`

Main function:

`run_pipeline(input_path)`

End-to-end test script:

`test_pipeline.py`

## 4. Run Management

Each pipeline execution receives a timestamp-based run ID.

All output files are stored in a separate run directory:

`outputs/pipeline_runs/<run_id>/`

The pipeline saves:

- `rubric_results.csv`
- `industry_results.csv`
- `scoring_results.csv`
- `outreach_results.csv`
- `run_summary.csv`

This prevents different pipeline runs from overwriting each other's outputs.

## 5. End-to-End Test

Input dataset:

`data/input/leads_full_scale_100.csv`

Test execution:

`python test_pipeline.py`

Observed run ID:

`20261031_212234`

Output directory:

`outputs/pipeline_runs/20261031_212234/`

## 6. Observed Results

| Metric                 | Result |
| ---------------------- | -----: |
| Input leads            |    100 |
| Rubric records         |    100 |
| Industry assessments   |    100 |
| Scored leads           |    100 |
| Qualified leads        |      5 |
| Review leads           |     93 |
| Rejected leads         |      2 |
| Outreach generated     |      5 |
| Outreach failures      |      0 |
| Average weighted score |   6.39 |

## 7. Validation

All expected output files were verified to exist.

All five pipeline stages completed successfully.

The industry assessment processed four batches of 25 leads each. Outreach generation processed the five qualified leads in one batch.

## 8. Engineering Decisions

- Modules remain separated by responsibility.
- The pipeline orchestrator controls execution order.
- Each execution receives a separate output directory.
- Intermediate results are preserved for debugging and auditability.
- Outreach is generated only for qualified leads.
- A run summary records key execution metrics.

## 9. Current Limitations

- Industry assessment and outreach require external NVIDIA API availability.
- Fresh LLM assessments may produce slightly different results between runs.
- Pipeline-level failure recovery and partial-stage resume are not yet implemented.
- Run metadata and detailed error logs can be improved.

# 02 — Data Understanding and Profiling

## 1. Dataset Overview

The project uses `leads_full_scale_100.csv` as its primary dataset for lead qualification and intelligence analysis.

The dataset contains 100 lead records representing prospective B2B customers across different industries, company sizes, and lead acquisition sources.

| Attribute         |                      Value |
| ----------------- | -------------------------: |
| Dataset file      | `leads_full_scale_100.csv` |
| Total records     |                        100 |
| Total columns     |                          6 |
| Missing values    |                          0 |
| Duplicate rows    |                          0 |
| Unique lead names |                        100 |
| Unique companies  |                        100 |

## 2. Dataset Schema

The original CSV contains six columns.

| Column                  | Data Type | Description                                 |
| ----------------------- | --------- | ------------------------------------------- |
| `name`                  | String    | Lead's name                                 |
| `company`               | String    | Lead's organization                         |
| `company_size`          | Integer   | Number of employees in the company          |
| `industry`              | String    | Industry in which the company operates      |
| `source`                | String    | Channel through which the lead was acquired |
| `last_interaction_date` | String    | Date of the most recent interaction         |

**Lead ID handling:** The original dataset does not contain a `lead_id` column. The pipeline generates lead IDs when they are not provided in the input.

## 3. Data Quality Assessment

Initial profiling was performed to understand completeness, uniqueness, and basic data validity.

| Quality Check             | Result | Observation                              |
| ------------------------- | -----: | ---------------------------------------- |
| Missing values            |      0 | All six columns are complete             |
| Duplicate rows            |      0 | No exact duplicate records               |
| Unique lead names         |    100 | Every lead has a unique name             |
| Unique companies          |    100 | Every lead belongs to a distinct company |
| Invalid interaction dates |      0 | All dates were successfully parsed       |

The initial dataset appears complete and free from exact duplicate records. Further business-rule validation is performed during pipeline execution.

## 4. Company Size Analysis

Company size represents the number of employees in each organization.

| Statistic          |    Value |
| ------------------ | -------: |
| Count              |      100 |
| Mean               |   473.81 |
| Standard deviation | 1,071.40 |
| Minimum            |        3 |
| 25th percentile    |    68.75 |
| Median             |      140 |
| 75th percentile    |   362.50 |
| Maximum            |    8,000 |

**Observation:** The dataset contains organizations ranging from very small businesses to large enterprises. The mean company size is considerably higher than the median, indicating that some large organizations influence the average.

## 5. Industry Distribution

The dataset contains 46 distinct industry categories.

Some of the most frequently represented industries are:

| Industry      | Lead Count |
| ------------- | ---------: |
| SaaS          |          7 |
| Retail        |          7 |
| Software      |          7 |
| Healthcare    |          6 |
| Logistics     |          5 |
| Finance       |          4 |
| Hospitality   |          3 |
| Cybersecurity |          3 |
| Energy        |          3 |
| Real Estate   |          3 |

The remaining industries have between one and two leads each.

**Observation:** The dataset has broad industry coverage rather than being concentrated in only a few sectors. This makes industry-fit assessment an important part of lead qualification.

## 6. Lead Source Distribution

There are six distinct lead acquisition sources.

| Lead Source          | Lead Count |
| -------------------- | ---------: |
| Inbound demo request |         19 |
| LinkedIn outreach    |         18 |
| Content download     |         17 |
| Sales call           |         17 |
| Referral             |         16 |
| Webinar attendee     |         13 |
| **Total**            |    **100** |

**Observation:** Lead sources are relatively balanced. Inbound demo requests represent the largest group, while webinar attendees represent the smallest group.

The source distribution allows the scoring engine to evaluate leads based on their acquisition intent.

## 7. Interaction Date Analysis

The `last_interaction_date` column contains the most recent interaction date for each lead.

| Attribute     | Value      |
| ------------- | ---------- |
| Earliest date | 2023-08-30 |
| Latest date   | 2024-01-20 |
| Invalid dates | 0          |

All interaction dates were successfully parsed during profiling.

**Important observation:** The dataset contains historical interaction dates. Recency scores therefore depend on the evaluation date used by the pipeline. Running the same dataset with different evaluation dates can produce different recency ratings and qualification outcomes.

## 8. Sample Records

The following records represent the structure of the original dataset:

| Name          | Company               | Company Size | Industry | Source               | Last Interaction |
| ------------- | --------------------- | -----------: | -------- | -------------------- | ---------------- |
| Alice Chen    | CloudScale AI         |           50 | SaaS     | Inbound demo request | 2024-01-15       |
| Bob Rodriguez | TechVentures Inc      |            8 | SaaS     | LinkedIn outreach    | 2024-01-20       |
| Carol Singh   | National Bank Corp    |        5,000 | Finance  | Content download     | 2023-12-01       |
| David Moore   | StartupXYZ            |            3 | SaaS     | Referral             | 2024-01-18       |
| Emma Thompson | RetailWorks Solutions |          200 | Retail   | Inbound demo request | 2023-11-10       |

## 9. Key Findings

1. The dataset contains 100 complete lead records across six input columns.
2. No missing values or exact duplicate rows were found during initial profiling.
3. Company sizes range from 3 to 8,000 employees.
4. The dataset contains 46 distinct industry categories.
5. Six different lead acquisition sources are represented.
6. Interaction dates range from August 2023 to January 2024.
7. Historical interaction dates make the evaluation date important for recency scoring.

## 10. Conclusion

The initial profiling indicates that the dataset is structurally complete and suitable for further processing.

However, completeness alone does not guarantee business validity. The pipeline performs additional validation of company size, lead source, interaction dates, and required lead information before generating qualification scores.

These profiling findings provide the foundation for the scoring rubric and data validation stages.

# 01 — Project Overview

## 1. Project Title

**Lead Intelligence Studio — AI-Powered B2B Lead Qualification and Outreach Platform**

## 2. Introduction

Lead Intelligence Studio is an AI-powered lead qualification platform designed to help B2B SaaS companies identify, evaluate, prioritize, and engage potential customers.

The system processes lead information from CSV files, applies rule-based business scoring, evaluates industry relevance using NVIDIA's Nemotron language model, calculates weighted qualification scores, and generates personalized outreach emails for qualified leads.

The application provides an interactive Streamlit dashboard to monitor lead qualification results, review priority leads, access generated outreach messages, and track historical pipeline executions.

## 3. Business Problem

B2B sales teams often receive leads from multiple sources, including demo requests, referrals, webinars, content downloads, and LinkedIn outreach.

Manually evaluating these leads can create several challenges:

- Time-consuming lead qualification.
- Inconsistent evaluation across sales representatives.
- Difficulty identifying high-potential companies.
- Limited prioritization of sales opportunities.
- Repetitive and generic outreach communication.
- Lack of centralized visibility into qualification results.

The business needs a structured and repeatable process to evaluate leads and help sales teams focus on the most promising opportunities.

## 4. Project Objectives

The primary objectives are:

1. Automate CSV-based lead ingestion and validation.
2. Evaluate company size, industry relevance, lead source, and interaction recency.
3. Use NVIDIA Nemotron LLM for industry-fit assessment.
4. Calculate weighted lead qualification scores.
5. Classify leads into qualified, review, and rejected categories.
6. Rank qualified leads according to their scores.
7. Generate personalized outreach emails for qualified leads.
8. Maintain independent pipeline execution records.
9. Provide an interactive dashboard for business analysis.
10. Support historical analysis and reliability testing.

## 5. Business Scenario

The project is designed around a hypothetical mid-market B2B SaaS company selling workflow automation software.

The sales team receives lead information through multiple acquisition channels and needs to determine which companies are most likely to benefit from its software.

The Lead Intelligence Studio acts as an automated qualification layer between lead acquisition and sales engagement.

## 6. Input Dataset

The system accepts lead information through CSV files.

The required input columns are:

| Column                | Description                            |
| --------------------- | -------------------------------------- |
| lead_id               | Unique lead identifier                 |
| name                  | Lead contact name                      |
| company               | Company name                           |
| company_size          | Number of employees                    |
| industry              | Industry in which the company operates |
| source                | Lead acquisition source                |
| last_interaction_date | Date of the most recent interaction    |

The project includes sample datasets for development, testing, and full-scale evaluation.

## 7. Solution Approach

The platform follows a multi-stage lead intelligence workflow:

1. **Lead Ingestion:** Accept CSV files and preserve uploaded originals.
2. **Data Validation:** Check required columns, lead identifiers, and input structure.
3. **Rule-Based Assessment:** Calculate company-size, lead-source, and recency ratings.
4. **AI Industry Assessment:** Evaluate industry relevance using NVIDIA Nemotron.
5. **Weighted Scoring:** Combine assessment dimensions using predefined weights.
6. **Lead Classification:** Assign qualified, review, or rejected decisions.
7. **Priority Ranking:** Rank qualified leads by weighted score.
8. **Outreach Generation:** Create personalized email drafts for qualified leads.
9. **Pipeline Storage:** Save results separately for each execution.
10. **Dashboard Reporting:** Present qualification metrics, priority queues, outreach, and run history.

## 8. Lead Scoring Methodology

The qualification system uses four dimensions:

| Dimension           |   Weight |
| ------------------- | -------: |
| Company Size        |      30% |
| Industry Fit        |      25% |
| Lead Source Intent  |      30% |
| Interaction Recency |      15% |
| **Total**           | **100%** |

The weighted score is calculated using these predefined weights.

### Qualification Decisions

| Weighted Score | Decision  |
| -------------- | --------- |
| 8.00–10.00     | Qualified |
| 5.00–7.99      | Review    |
| Below 5.00     | Rejected  |

Critical missing or invalid data and industry assessments requiring manual review can override the score and result in a review decision.

## 9. Technology Stack

| Technology                   | Purpose                                                |
| ---------------------------- | ------------------------------------------------------ |
| Python                       | Core application and pipeline development              |
| Pandas                       | Data processing and transformation                     |
| NVIDIA Nemotron              | AI-powered industry assessment and outreach generation |
| OpenAI-compatible API client | Integration with NVIDIA API                            |
| Streamlit                    | Interactive web dashboard                              |
| python-dotenv                | Environment configuration                              |
| CSV                          | Input and pipeline result storage                      |
| Git                          | Version control                                        |

## 10. Application Features

The Streamlit application provides the following sections:

### Dashboard

Displays:

- Total leads.
- Qualified leads.
- Leads requiring review.
- Rejected leads.
- Average lead score.
- Outreach generation count.
- Qualification and source distributions.
- Top priority leads.

### Upload Leads

Allows users to upload CSV files, preview the dataset, and execute the complete lead intelligence pipeline.

### Priority Queue

Displays qualified leads ranked by their priority scores.

### Outreach

Provides access to personalized outreach email drafts generated for qualified leads.

### Run History

Displays previous pipeline executions, including lead counts, qualification decisions, and average scores.

### Pipeline Run Selection

Allows users to select different pipeline runs and view their corresponding results.

## 11. Reliability and Testing

The project includes 10 reliability experiments covering:

- Idempotency and run isolation.
- Missing required columns.
- Empty CSV handling.
- Duplicate, missing, and blank lead IDs.
- Invalid business data.
- No-qualified-lead scenarios.
- API retry handling.
- Output integrity and reconciliation.

All 10 implemented reliability experiments passed.

An additional historical simulation was conducted to study the impact of evaluation dates on lead qualification outcomes.

## 12. Project Scope

### Included

- CSV-based lead ingestion.
- Input validation.
- Rule-based lead assessment.
- NVIDIA-powered industry assessment.
- Weighted scoring and classification.
- Qualified lead prioritization.
- AI-generated outreach drafts.
- Independent pipeline run storage.
- Interactive Streamlit dashboard.
- Historical simulation and reliability testing.

### Current Limitations

- The application uses CSV-based input rather than a live CRM integration.
- Lead qualification depends on the quality and completeness of supplied data.
- LLM-generated assessments can vary between independent API executions.
- Outreach messages are generated as drafts; automated email delivery is not implemented.
- Production-scale concurrency and deployment performance have not been established.

## 13. Expected Business Value

The Lead Intelligence Studio aims to:

- Reduce manual lead qualification effort.
- Improve consistency in sales prioritization.
- Identify promising business opportunities more efficiently.
- Support industry-aware lead evaluation.
- Reduce repetitive outreach drafting.
- Improve visibility into lead qualification performance.
- Maintain traceable records of pipeline executions.

## 14. Conclusion

Lead Intelligence Studio demonstrates how rule-based data processing and generative AI can be combined to build an automated B2B lead qualification workflow.

By integrating data validation, AI-powered industry assessment, weighted scoring, lead prioritization, personalized outreach, and interactive reporting, the platform provides a structured foundation for more efficient sales lead management.

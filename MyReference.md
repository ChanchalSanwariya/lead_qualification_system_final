# Lead Intelligence Studio

A local Streamlit-based application that helps businesses analyze, qualify, rank, and engage B2B leads using rule-based scoring and NVIDIA AI-powered industry assessment.

## 1. Project Overview

Lead Intelligence Studio automates the lead qualification process.

It takes lead data in CSV format and performs the following steps:

1. Loads and validates lead data.
2. Evaluates company size, lead source, and interaction recency.
3. Uses NVIDIA AI to assess industry fit.
4. Calculates a weighted qualification score.
5. Classifies leads as Qualified, Review, or Rejected.
6. Ranks qualified leads by score.
7. Generates personalized outreach email drafts for qualified leads.
8. Saves pipeline results for future analysis.

The application runs locally using Streamlit.

## 2. Project Structure

```text
lead_qualification_system_final/
│
├── data/
│   └── input/                 # Sample and testing CSV datasets
│
├── docs/                      # Project documentation
│
├── landing/                   # Original uploaded CSV files
│
├── outputs/
│   └── pipeline_runs/         # Saved pipeline results
│
├── src/
│   ├── industry.py            # AI-based industry assessment
│   ├── outreach.py            # Outreach email generation
│   ├── pipeline.py            # End-to-end pipeline
│   ├── rubric.py              # Rule-based evaluation
│   ├── scoring.py             # Weighted scoring and decisions
│   └── utils.py               # Shared utility functions
│
├── test/                      # Testing scripts
│
├── .env                       # Local environment configuration
├── .env.example               # Example configuration
├── app.py                     # Streamlit application
├── requirements.txt           # Project dependencies
└── README.md                  # Project guide
```

## 3. Prerequisites

Before running the project, make sure you have:

- Python installed
- VS Code or another Python editor
- NVIDIA API key
- Project dependencies installed

## 4. Project Setup

### Step 1: Open the project

Open the project folder in VS Code.

### Step 2: Install dependencies

If you are using `uv`, run:

```powershell
uv sync
```

Alternatively, install dependencies from `requirements.txt`:

```powershell
pip install -r requirements.txt
```

### Step 3: Configure the API key

Create your local `.env` file using `.env.example` as a reference.

Add your NVIDIA API key:

```env
NVIDIA_API_KEY=your_nvidia_api_key
```

Keep your actual API key private. Never upload `.env` to GitHub or share it publicly.

Make sure the other configuration values in `.env` match the settings expected by the project.

## 5. Run the Application

Open the VS Code terminal in the project root directory.

Run:

```powershell
uv run streamlit run app.py
```

Streamlit will start the application.

Open the local URL shown in the terminal, usually:

```text
http://localhost:8501
```

## 6. How to Use the Application

The application contains five main sections.

### A. Dashboard

The Dashboard provides an overview of a selected pipeline run.

You can view:

- Total leads processed
- Qualified leads
- Leads requiring review
- Rejected leads
- Average lead score
- Lead distribution and scoring charts
- Top-priority leads

**How to view old results:**

1. Open the Dashboard.
2. Find the pipeline run selector.
3. Select an existing run from the available runs.
4. The dashboard will display the saved results for that run.

You do not need to upload the same CSV again to view an existing run.

### B. Upload Leads

Use this section when you want to analyze a new CSV file.

Steps:

1. Open **Upload Leads**.
2. Select your CSV file.
3. Review the uploaded data preview.
4. Start the pipeline.
5. Wait for validation, scoring, industry assessment, and outreach generation to finish.
6. Review the generated summary.

Each upload creates a separate pipeline run. Previous runs are preserved and are not intentionally overwritten.

The original uploaded CSV is stored in the `landing/` directory.

### C. Priority Queue

This section displays qualified leads in priority order.

You can review lead details, qualification scores, and reasoning to identify which leads should receive attention first.

### D. Outreach

This section displays the generated outreach email drafts for qualified leads.

You can review the email subject and body before using them.

**Important:** AI-generated emails are drafts. Review factual claims and personalization before sending them to anyone.

### E. Run History

Use this section to browse previously saved pipeline runs and review their execution results.

Each run has its own output directory, making it easier to compare different uploads and analyses.

## 7. Understanding Saved Results

Pipeline results are stored under:

```text
outputs/pipeline_runs/
```

Each run has a separate folder containing files such as:

| File                   | Purpose                               |
| ---------------------- | ------------------------------------- |
| `rubric_results.csv`   | Rule-based evaluation results         |
| `industry_results.csv` | AI-based industry assessment          |
| `scoring_results.csv`  | Final scores, decisions, and rankings |
| `outreach_results.csv` | Generated outreach email drafts       |
| `run_summary.csv`      | Overall pipeline summary              |

The original uploaded CSV is stored separately under `landing/`.

**To inspect a previous result manually:** Open the corresponding run folder and view its CSV files in VS Code or Excel.

## 8. Lead Qualification Logic

The application uses a weighted scoring model.

| Evaluation factor   |   Weight |
| ------------------- | -------: |
| Company Size        |      30% |
| Industry Fit        |      25% |
| Lead Source         |      30% |
| Interaction Recency |      15% |
| **Total**           | **100%** |

The final weighted score determines the lead's qualification decision.

| Score      | Decision  |
| ---------- | --------- |
| 8.00–10.00 | Qualified |
| 5.00–7.99  | Review    |
| Below 5.00 | Rejected  |

Certain missing or invalid data and AI assessment flags can override the score and place a lead in Review.

## 9. Input CSV Format

The CSV should contain these required columns:

| Column                  | Description                  |
| ----------------------- | ---------------------------- |
| `name`                  | Lead's name                  |
| `company`               | Company name                 |
| `company_size`          | Number of employees          |
| `industry`              | Company's industry           |
| `source`                | How the lead was acquired    |
| `last_interaction_date` | Date of the last interaction |

The `lead_id` column is optional. If it is not provided, the application generates lead IDs. If provided, IDs must be valid and unique.

## 10. Testing

Test scripts are available in the `test/` directory.

For example, to run the outreach test:

```powershell
uv run python -m test.test_outreach
```

Run commands from the project root directory so Python can locate the `src` package.

## 11. Important Notes

- Keep your `.env` file private.
- Use the expected CSV column names.
- Review generated email drafts before sending.
- Do not manually modify saved pipeline results if you want to preserve the original run output.
- Each new upload should create a separate run.
- Previously saved results can be viewed without running the pipeline again.

## 12. Quick Start

For someone using the project for the first time:

```powershell
uv sync
uv run streamlit run app.py
```

Then open `http://localhost:8501`.

- To see previous analysis: Go to **Dashboard** and select an existing run.
- To analyze new leads: Go to **Upload Leads** and upload a CSV.
- To see ranked qualified leads: Open **Priority Queue**.
- To review generated emails: Open **Outreach**.
- To browse previous executions: Open **Run History**.

---

**Lead Intelligence Studio — From raw lead data to actionable sales priorities.**

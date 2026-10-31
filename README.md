# Lead Intelligence Studio

**An AI-powered B2B Lead Qualification and Prioritization System**

Lead Intelligence Studio automates lead evaluation using rule-based scoring and NVIDIA Nemotron AI. It processes leads in batches, calculates qualification scores, ranks qualified leads, and generates personalized outreach email drafts.

## 1. Setup and Run

**Prerequisites:** Python, project dependencies, and a valid NVIDIA API key.

1. Clone or download the project and open its root folder in VS Code.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file using `.env.example` as a reference and configure:

   ```env
   NVIDIA_API_KEY=your_nvidia_api_key
   ```

4. Start the application:

   ```bash
   streamlit run app.py
   ```

5. Open `http://localhost:8501` in your browser.

## 2. How to Use

- **Dashboard:** View lead statistics, charts, and results from previous pipeline runs. Select an existing run to inspect its saved analysis without uploading the file again.
- **Upload Leads:** Upload a new CSV to start an independent pipeline run. Original uploads and previous results are preserved.
- **Priority Queue:** View qualified leads ranked by score.
- **Outreach:** Review AI-generated personalized email drafts.
- **Run History:** Browse previously executed pipeline runs.

## 3. Input Data

CSV files must contain these columns:

`name`, `company`, `company_size`, `industry`, `source`, `last_interaction_date`

`lead_id` is optional and generated when missing. Provided IDs must be valid and unique.

## 4. Qualification Rubric

Leads receive a weighted score from 1–10 using four factors: Company Size (30%), Industry Fit (25%), Lead Source (30%), and Interaction Recency (15%). Industry Fit is assessed using NVIDIA Nemotron AI, while the other factors use predefined business rules.

| Score   | Decision  |
| ------- | --------- |
| 8–10    | Qualified |
| 5–7.99  | Review    |
| Below 5 | Rejected  |

Missing or invalid critical data and AI review flags can override the score and place a lead in Review.

## 5. Outputs

Each pipeline run saves results under `outputs/pipeline_runs/`:

- `scoring_results.csv` – Qualification score, decision, reasoning, and priority rank.
- `industry_results.csv` – AI industry assessment.
- `rubric_results.csv` – Rule-based evaluation.
- `outreach_results.csv` – Generated email drafts.
- `run_summary.csv` – Aggregated pipeline statistics.

Original uploaded CSV files are stored under `landing/`.

## 6. Reliability and Error Handling

The pipeline processes leads in batches rather than making one API call per lead. API failures and rate limits are handled using retries with exponential backoff. Input validation checks missing columns, empty files, and invalid or duplicate lead IDs. Failed AI assessments and incomplete data are handled through review or failure statuses.

## 7. Known Limitations

- Industry assessments and outreach messages depend on LLM responses and may require human review.
- AI-generated emails are drafts, not messages automatically sent to prospects.
- Missing or invalid business information may result in a Review decision.
- API availability, rate limits, and network connectivity can affect processing time.
- Company size and lead-source ratings use predefined scoring rules.

**Technology:** Python · Pandas · Streamlit · NVIDIA Nemotron API

**Project Goal:** Transform raw lead data into actionable sales priorities.

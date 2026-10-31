
import streamlit as st
import pandas as pd

from pathlib import Path
from src.utils import (
    initialize_project_folders,
    generate_run_id,
    create_run_directories,
    save_uploaded_file
)

from src.pipeline import run_pipeline

# --------------------------------------------------
# 1. Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Lead Intelligence Studio",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)



# --------------------------------------------------
# 2. Project Initialization
# --------------------------------------------------

initialize_project_folders()

PROJECT_ROOT = Path(__file__).resolve().parent

PIPELINE_RUNS_DIR = (
    PROJECT_ROOT
    / "outputs"
)


# --------------------------------------------------
# 3. Discover and Load Pipeline Runs
# --------------------------------------------------


def discover_pipeline_runs():

    run_folders = []

    if not PIPELINE_RUNS_DIR.exists():
        return run_folders

    for summary_file in PIPELINE_RUNS_DIR.rglob("run_summary.csv"):

        run_dir = summary_file.parent

        scoring_file = run_dir / "scoring_results.csv"
        outreach_file = run_dir / "outreach_results.csv"

        if scoring_file.exists() and outreach_file.exists():

            run_folders.append(run_dir)

    return sorted(
        run_folders,
        key=lambda folder: folder.stat().st_mtime,
        reverse=True
    )


@st.cache_data
def load_run_data(run_dir):

    run_dir = Path(run_dir)

    scoring = pd.read_csv(
        run_dir / "scoring_results.csv"
    )

    outreach = pd.read_csv(
        run_dir / "outreach_results.csv"
    )

    summary = pd.read_csv(
        run_dir / "run_summary.csv"
    )

    return scoring, outreach, summary


available_runs = discover_pipeline_runs()

if not available_runs:

    st.error("No completed pipeline runs found.")
    st.stop()


# --------------------------------------------------
# 4. Select Pipeline Run
# --------------------------------------------------

run_options = {
    str(folder.relative_to(PIPELINE_RUNS_DIR)): folder
    for folder in available_runs
}

selected_run_label = st.sidebar.selectbox(
    "Select Pipeline Run",
    options=list(run_options.keys())
)

selected_run_dir = run_options[selected_run_label]

try:

    scoring_df, outreach_df, summary_df = load_run_data(
        str(selected_run_dir)
    )

except Exception as error:

    st.error(f"Unable to load pipeline results: {error}")
    st.stop()


summary = dict(
    zip(summary_df["metric"], summary_df["value"])
)

selected_run_id = summary["run_id"]


# --------------------------------------------------
# 4. Sidebar Navigation
# --------------------------------------------------

with st.sidebar:

    st.title("🎯 Lead Intelligence Studio")

    st.caption("B2B Lead Qualification Platform")

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "Dashboard",
            "Upload Leads",
            "Priority Queue",
            "Outreach",
            "Run History"
        ]
    )

    st.divider()

    st.caption("Powered by Python, Streamlit & NVIDIA AI")


# --------------------------------------------------
# 5. Dashboard Page
# --------------------------------------------------

if page == "Dashboard":

    st.title("Lead Intelligence Dashboard")

    st.caption(
        f"Selected analysis | Run ID: {selected_run_id}"
    )

    st.divider()

    # KPI Calculations

    total_leads = int(summary["total_leads"])

    qualified = int(summary["qualified"])

    review = int(summary["review"])

    rejected = int(summary["rejected"])

    avg_score = float(summary["average_weighted_score"])

    outreach_generated = int(summary["outreach_generated"])


    # KPI Cards

    st.subheader("Business Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Leads",
        total_leads
    )

    col2.metric(
        "Qualified Leads",
        qualified
    )

    col3.metric(
        "Needs Review",
        review
    )

    col4.metric(
        "Rejected Leads",
        rejected
    )

    col5, col6 = st.columns(2)

    col5.metric(
        "Average Lead Score",
        f"{avg_score:.2f}/10"
    )

    col6.metric(
        "Outreach Generated",
        outreach_generated
    )

    st.divider()


    # Decision Distribution

    st.subheader("Lead Qualification Distribution")

    decision_counts = (
        scoring_df["decision"]
        .value_counts()
        .reindex(
            ["qualified", "review", "rejected"],
            fill_value=0
        )
    )

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:

        st.markdown("**Lead Decision Breakdown**")

        st.bar_chart(decision_counts)

    with chart_col2:

        st.markdown("**Lead Source Distribution**")

        source_counts = scoring_df["source"].value_counts()

        st.bar_chart(source_counts)


    st.divider()


    # Top Priority Leads

    st.subheader("Top Priority Leads")

    top_leads = (
        scoring_df[
            scoring_df["decision"] == "qualified"
        ]
        .sort_values("priority_rank")
        .head(10)
    )

    display_columns = [
        "priority_rank",
        "name",
        "company",
        "industry",
        "weighted_score",
        "decision"
    ]

    st.dataframe(
        top_leads[display_columns],
        use_container_width=True,
        hide_index=True
    )


# --------------------------------------------------
# 6. Upload Leads Page
# --------------------------------------------------

elif page == "Upload Leads":

    st.title("Upload Lead Dataset")

    st.write(
        "Upload a CSV file to execute the complete "
        "lead intelligence pipeline."
    )

    uploaded_file = st.file_uploader(
        "Choose your lead CSV file",
        type=["csv"],
        key="lead_csv_upload"
    )

    if uploaded_file is not None:

        st.success(
            f"File selected: {uploaded_file.name}"
        )

        try:

            preview_df = pd.read_csv(
                uploaded_file
            )

            st.subheader("File Preview")

            st.dataframe(
                preview_df.head(10),
                use_container_width=True,
                hide_index=True
            )

            st.caption(
                f"Total rows: {len(preview_df)}"
            )

            if st.button(
                "Run Lead Intelligence Pipeline",
                type="primary"
            ):

                with st.spinner(
                    "Executing lead intelligence pipeline..."
                ):

                    # Generate unique run ID
                    run_id = generate_run_id(
                        uploaded_file.name
                    )

                    # Create separate directories
                    landing_path, output_path = (
                        create_run_directories(run_id)
                    )

                    # Save original uploaded CSV
                    uploaded_file.seek(0)

                    saved_file = save_uploaded_file(
                        uploaded_file.getvalue(),
                        uploaded_file.name,
                        landing_path
                    )

                    # Execute pipeline
                    result = run_pipeline(
                        input_path=saved_file,
                        run_id=run_id,
                        output_dir=output_path
                    )

                st.success(
                    "Pipeline executed successfully!"
                )

                st.write("Run ID:", run_id)

                st.write(
                    "Output directory:",
                    str(output_path)
                )

                st.subheader("Execution Summary")

                result_summary = result["summary"]

                st.dataframe(
                    result_summary,
                    use_container_width=True,
                    hide_index=True
                )

                st.info(
                    "Refresh the application to see this "
                    "run in the pipeline run selector."
                )

        except Exception as error:

            st.error(
                f"Upload or pipeline execution failed: {error}"
            )



# --------------------------------------------------
# 7. Priority Queue Page
# --------------------------------------------------

elif page == "Priority Queue":

    st.title("Qualified Lead Priority Queue")

    qualified_leads = scoring_df[
        scoring_df["decision"] == "qualified"
    ].sort_values("priority_rank")

    st.dataframe(
        qualified_leads[
            [
                "priority_rank",
                "name",
                "company",
                "industry",
                "weighted_score",
                "decision_reasoning"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )


# --------------------------------------------------
# 8. Outreach Page
# --------------------------------------------------

elif page == "Outreach":

    st.title("Personalized Outreach")

    st.caption(
        f"{len(outreach_df)} outreach messages generated"
    )

    for _, row in outreach_df.iterrows():

        with st.expander(
            f"{row['name']} — {row['company']}"
        ):

            st.markdown(
                f"**Subject:** {row['subject']}"
            )

            st.text_area(
                "Email Body",
                value=row["email_body"],
                height=220,
                key=f"email_{row['lead_id']}"
            )


# --------------------------------------------------
# 9. Run History Page
# --------------------------------------------------

elif page == "Run History":

    st.title("Pipeline Run History")

    history_records = []

    for run_dir in available_runs:

        try:
            _, _, run_summary_df = load_run_data(str(run_dir))

            run_summary = dict(
                zip(
                    run_summary_df["metric"],
                    run_summary_df["value"]
                )
            )

            history_records.append({
                "Run ID": run_summary["run_id"],
                "Run Type": run_dir.parent.name
                    if run_dir.parent != PIPELINE_RUNS_DIR
                    else "Standard",
                "Total Leads": int(run_summary["total_leads"]),
                "Qualified": int(run_summary["qualified"]),
                "Review": int(run_summary["review"]),
                "Rejected": int(run_summary["rejected"]),
                "Average Score": float(
                    run_summary["average_weighted_score"]
                ),
                "Outreach Generated": int(
                    run_summary["outreach_generated"]
                )
            })

        except Exception as error:
            st.warning(f"Could not read {run_dir.name}: {error}")

    history_df = pd.DataFrame(history_records)

    st.dataframe(
        history_df,
        use_container_width=True,
        hide_index=True
    )

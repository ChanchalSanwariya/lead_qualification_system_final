
import os
import re
from datetime import datetime
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv


# --------------------------------------------------
# 1. PROJECT PATHS
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

ENV_FILE = PROJECT_ROOT / ".env"

load_dotenv(ENV_FILE)


# --------------------------------------------------
# 2. ENVIRONMENT CONFIGURATION
# --------------------------------------------------

def get_config():
    """
    Read application configuration dynamically from .env.
    """

    return {
        "nvidia_api_key": os.getenv("NVIDIA_API_KEY", "").strip(),

        "base_url": os.getenv(
            "NVIDIA_BASE_URL",
            "https://integrate.api.nvidia.com/v1"
        ).strip(),

        "model": os.getenv(
            "NVIDIA_MODEL",
            "nvidia/nemotron-3.5-lightning-30b-a3b"
        ).strip(),

        "landing_dir": PROJECT_ROOT / os.getenv(
            "LANDING_DIR", "landing"
        ),

        "outputs_dir": PROJECT_ROOT / os.getenv(
            "OUTPUTS_DIR", "outputs"
        ),

        "industry_batch_size": int(
            os.getenv("INDUSTRY_BATCH_SIZE", "25")
        ),

        "outreach_batch_size": int(
            os.getenv("OUTREACH_BATCH_SIZE", "10")
        ),

        "max_retries": int(
            os.getenv("API_MAX_RETRIES", "3")
        ),

        "evaluation_date": os.getenv(
            "EVALUATION_DATE", ""
        ).strip(),
    }


# --------------------------------------------------
# 3. REQUIRED CSV COLUMNS
# --------------------------------------------------

REQUIRED_COLUMNS = [
    "name",
    "company",
    "company_size",
    "industry",
    "source",
    "last_interaction_date",
]


# --------------------------------------------------
# 4. SAFE FILE AND FOLDER NAMES
# --------------------------------------------------

def safe_name(value):
    """
    Convert a filename into a safe folder-name format.
    """

    value = str(value).strip().lower()

    value = re.sub(
        r"[^a-z0-9_-]+",
        "_",
        value
    )

    return value.strip("_") or "uploaded_leads"


# --------------------------------------------------
# 5. GENERATE UNIQUE RUN ID
# --------------------------------------------------

def generate_run_id(filename):
    """
    Create a unique timestamp-based run ID.
    """

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S_%f"
    )

    file_name = safe_name(
        Path(filename).stem
    )

    return f"{timestamp}_{file_name}"


# --------------------------------------------------
# 6. CREATE RUN FOLDERS
# --------------------------------------------------

def create_run_directories(run_id):
    """
    Create separate landing and pipeline output folders.
    """

    config = get_config()

    landing_path = (
        config["landing_dir"] / run_id
    )

    output_path = (
        config["outputs_dir"]
        / "pipeline_runs"
        / run_id
    )

    landing_path.mkdir(
        parents=True,
        exist_ok=False
    )

    output_path.mkdir(
        parents=True,
        exist_ok=False
    )

    return landing_path, output_path


# --------------------------------------------------
# 7. SAVE ORIGINAL UPLOADED FILE
# --------------------------------------------------

def save_uploaded_file(
    file_bytes,
    filename,
    landing_path
):
    """
    Save original uploaded CSV without modifying it.
    """

    safe_filename = safe_name(
        Path(filename).stem
    ) + ".csv"

    file_path = landing_path / safe_filename

    file_path.write_bytes(file_bytes)

    return file_path


# --------------------------------------------------
# 8. LOAD AND VALIDATE CSV
# --------------------------------------------------

def load_and_validate_csv(file_path):
    """
    Read CSV and validate required columns and lead IDs.
    """

    file_path = Path(file_path)

    if not file_path.exists():
        raise FileNotFoundError(
            f"CSV file not found: {file_path}"
        )

    try:
        df = pd.read_csv(file_path)

    except Exception as error:
        raise ValueError(
            f"Unable to read CSV: {error}"
        ) from error

    if df.empty:
        raise ValueError(
            "Uploaded CSV contains no lead records."
        )

    # Normalize column names.
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
    )

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    # Generate IDs if they are not provided.
    if "lead_id" not in df.columns:

        df.insert(
            0,
            "lead_id",
            [
                f"LEAD_{i:04d}"
                for i in range(1, len(df) + 1)
            ]
        )

    else:

        df["lead_id"] = (
            df["lead_id"]
            .astype("string")
            .str.strip()
        )

        if df["lead_id"].isna().any():
            raise ValueError(
                "lead_id contains missing values."
            )

        if df["lead_id"].eq("").any():
            raise ValueError(
                "lead_id contains empty values."
            )

        if df["lead_id"].duplicated().any():
            raise ValueError(
                "Duplicate lead_id values found."
            )

    return df


# --------------------------------------------------
# 9. CREATE REQUIRED APPLICATION FOLDERS
# --------------------------------------------------

def initialize_project_folders():
    """
    Create application folders if they do not exist.
    """

    config = get_config()

    folders = [
        config["landing_dir"],
        config["outputs_dir"],
        PROJECT_ROOT / "data" / "input",
        PROJECT_ROOT / "docs",
    ]

    for folder in folders:
        folder.mkdir(
            parents=True,
            exist_ok=True
        )

    return True

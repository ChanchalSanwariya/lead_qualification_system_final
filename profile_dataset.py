
import pandas as pd
from pathlib import Path

file_path = Path("data/input/leads_full_scale_100.csv")

df = pd.read_csv(file_path)

print("\n========== DATASET OVERVIEW ==========")

print("File:", file_path)
print("Total rows:", len(df))
print("Total columns:", len(df.columns))

print("\n========== COLUMN INFORMATION ==========")

print(df.dtypes)

print("\n========== MISSING VALUES ==========")

print(df.isnull().sum())

print("\n========== DUPLICATE RECORDS ==========")

print("Duplicate rows:", df.duplicated().sum())

if "lead_id" in df.columns:
    print(
        "Duplicate lead IDs:",
        df["lead_id"].duplicated().sum()
    )

print("\n========== UNIQUE VALUES ==========")

for column in df.columns:
    print(
        f"{column}: {df[column].nunique()} unique values"
    )

print("\n========== INDUSTRY DISTRIBUTION ==========")

if "industry" in df.columns:
    print(df["industry"].value_counts(dropna=False))

print("\n========== LEAD SOURCE DISTRIBUTION ==========")

if "source" in df.columns:
    print(df["source"].value_counts(dropna=False))

print("\n========== COMPANY SIZE STATISTICS ==========")

if "company_size" in df.columns:
    print(
        pd.to_numeric(
            df["company_size"],
            errors="coerce"
        ).describe()
    )

print("\n========== INTERACTION DATE RANGE ==========")

if "last_interaction_date" in df.columns:

    dates = pd.to_datetime(
        df["last_interaction_date"],
        errors="coerce"
    )

    print("Earliest:", dates.min())
    print("Latest:", dates.max())
    print("Invalid dates:", dates.isna().sum())

print("\n========== SAMPLE RECORDS ==========")

print(df.head(5).to_string(index=False))

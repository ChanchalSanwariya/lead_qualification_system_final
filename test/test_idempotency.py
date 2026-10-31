from src.pipeline import run_pipeline
from pathlib import Path
import time

input_file = "data/input/leads_full_scale_100.csv"

print("\n========== IDEMPOTENCY TEST ==========")

# First run
print("\nStarting first pipeline run...")
run_1 = run_pipeline(input_file)

# Second run
print("\nStarting second pipeline run...")
run_2 = run_pipeline(input_file)

dir_1 = Path(run_1["run_dir"])
dir_2 = Path(run_2["run_dir"])

print("\n========== TEST RESULTS ==========")

print("Run 1 ID:", run_1["run_id"])
print("Run 2 ID:", run_2["run_id"])

print("Run 1 directory exists:", dir_1.exists())
print("Run 2 directory exists:", dir_2.exists())

print("Directories are different:", dir_1 != dir_2)

print("Run 1 lead count:", len(run_1["scoring_results"]))
print("Run 2 lead count:", len(run_2["scoring_results"]))

print(
    "Run 1 scoring file exists:",
    (dir_1 / "scoring_results.csv").exists()
)

print(
    "Run 2 scoring file exists:",
    (dir_2 / "scoring_results.csv").exists()
)

assert dir_1 != dir_2
assert dir_1.exists() and dir_2.exists()
assert len(run_1["scoring_results"]) == 100
assert len(run_2["scoring_results"]) == 100

print("\nTEST PASSED: Separate runs created without overwriting.")

import pandas as pd
from unittest.mock import patch, Mock

from src.outreach import generate_outreach

print("\n========== TEST 9: API RETRY MECHANISM ==========")

scoring_results = pd.DataFrame({
    "lead_id": ["LEAD_0001"],
    "name": ["John Smith"],
    "company": ["ABC Technologies"],
    "decision": ["qualified"],
})

# Simulate two failures followed by one successful response.
successful_response = [
    {
        "lead_id": "LEAD_0001",
        "subject": "Workflow automation for ABC Technologies",
        "email_body": "Hello John, let's discuss workflow automation.",
        "generation_status": "completed",
    }
]

mock_batch = Mock(
    side_effect=[
        RuntimeError("Simulated temporary API failure"),
        RuntimeError("Simulated rate limit error"),
        successful_response,
    ]
)

with patch("src.outreach.get_config", return_value={
    "outreach_batch_size": 10,
    "max_retries": 3,
}), patch("src.outreach.create_client", return_value=Mock()), \
     patch("src.outreach.generate_outreach_batch", mock_batch), \
     patch("src.outreach.time.sleep") as mock_sleep:

    results = generate_outreach(scoring_results)

print("\n========== TEST RESULTS ==========")

print("API attempts:", mock_batch.call_count)
print("Successful outreach records:", len(results))
print("Generation status:", results["generation_status"].tolist())

assert mock_batch.call_count == 3
assert len(results) == 1
assert results.iloc[0]["generation_status"] == "completed"

# Two failures mean two retry waits.
assert mock_sleep.call_count == 2

print("\nTEST PASSED: Retry mechanism recovered after two failures.")

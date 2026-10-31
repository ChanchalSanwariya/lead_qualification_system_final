# 06 — Personalized Outreach Generation

## 1. Objective

The objective of this module is to generate personalized B2B sales outreach emails for qualified leads.

Only leads with the final decision `qualified` are eligible for outreach generation.

Review and rejected leads are excluded from automated outreach generation.

The module generates email subjects and bodies but does not send emails.

## 2. Implementation

The outreach generation logic is implemented in:

`src/outreach.py`

Main function:

`generate_outreach(scoring_results)`

The module performs the following operations:

1. Filters qualified leads from scoring results.
2. Groups eligible leads into batches.
3. Sends batch requests to the NVIDIA LLM.
4. Generates personalized email subjects and bodies.
5. Validates returned lead IDs and email content.
6. Retries failed API requests.
7. Preserves failed generation statuses.
8. Returns structured outreach results.

If no qualified leads are available, outreach generation is skipped without making an unnecessary API request.

## 3. AI Model and Configuration

The module uses the configured NVIDIA model:

`nvidia/nemotron-3.5-lightning-30b-a3b`

The API is accessed through the OpenAI-compatible NVIDIA endpoint.

The outreach batch size is controlled through:

`OUTREACH_BATCH_SIZE`

The module uses:

- Structured JSON response formatting
- Disabled model thinking
- Configured API retry handling
- Environment-based API configuration

API credentials are loaded from environment variables and are not hardcoded in the source code.

## 4. Email Generation Rules

The prompt instructs the model to:

- Address leads by first name.
- Personalize messaging using company and industry information.
- Consider the lead source.
- Explain relevant workflow automation use cases.
- Avoid invented company facts and unsupported claims.
- Use a professional and concise tone.
- Include a low-pressure call to action.

### Factual Grounding

Generated emails must only use information supported by the available lead data or explicitly provided business context.

The model must not:

- Claim that a demo or walkthrough has already been prepared.
- Promise a recording or other deliverable that the application cannot provide.
- Claim that an action has been completed when it has not.
- Invent customer references, results, integrations, or company-specific facts.
- Make unsupported promises about product capabilities.

The outreach module generates draft emails only. Human review and approval are required before sending.

## 5. Testing

Test script:

`test_outreach.py`

Input:

`outputs/scoring_reproducible_output.csv`

Output:

`outputs/outreach_test_output.csv`

The test dataset contained 100 leads, of which five were qualified.

All five qualified leads were processed in one batch.

## 6. Test Results

| Metric                 | Result |
| ---------------------- | -----: |
| Qualified leads        |      5 |
| Total outreach records |      5 |
| Successfully generated |      5 |
| Failed                 |      0 |
| Duplicate lead IDs     |      0 |
| Empty subjects         |      0 |
| Empty email bodies     |      0 |
| API batches            |      1 |

## 7. Quality Observations

The generated emails used lead names, company names, and industry context for personalization.

However, technical validation alone does not guarantee factual accuracy.

During testing, one generated email included claims about a prepared walkthrough and a future recording. These actions had not been performed by the application.

This exposed a limitation in the initial prompt instructions.

The prompt therefore requires stronger factual-grounding rules to prevent unsupported commitments and claims about actions that have not occurred.

This finding demonstrates why generated content requires qualitative review in addition to technical validation.

## 8. Engineering Decisions

- Outreach is generated only for qualified leads.
- Review and rejected leads are excluded.
- Batch processing reduces the number of API requests.
- Structured JSON responses simplify output validation.
- Retry handling improves resilience against temporary API failures.
- Generated emails are saved as CSV records for inspection.
- The application does not automatically send generated emails.
- Human approval is required before any outreach is sent.

## 9. Future Improvements

- Strengthen factual-grounding rules in the generation prompt.
- Add automated checks for unsupported promises and claims.
- Evaluate email relevance and personalization quality.
- Introduce a human approval workflow before sending emails.
- Track outreach performance if email delivery integration is introduced.

## 10. Conclusion

The outreach generation module converts qualified leads into personalized email drafts using NVIDIA's LLM.

By restricting generation to qualified leads, processing requests in batches, validating structured responses, and preserving generation statuses, the module provides a controlled approach to AI-assisted sales outreach.

The testing process also highlighted the importance of factual accuracy and human approval when generating customer-facing content.

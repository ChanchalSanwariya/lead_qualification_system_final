# 03 — Lead Qualification Rubric Design

## 1. Objective

The lead qualification rubric converts raw lead information into a structured qualification score.

The system evaluates each lead using four dimensions:

1. Company Size
2. Industry Fit
3. Lead Source Intent
4. Interaction Recency

Each dimension contributes a predefined weight to the final score.

The final score ranges from 1 to 10.

## 2. Scoring Dimensions and Weights

| Dimension           |   Weight | Evaluation Method     |
| ------------------- | -------: | --------------------- |
| Company Size        |      30% | Rule-based            |
| Industry Fit        |      25% | NVIDIA LLM assessment |
| Lead Source Intent  |      30% | Rule-based            |
| Interaction Recency |      15% | Rule-based            |
| **Total**           | **100%** |                       |

Company size and lead source are evaluated using predefined business rules. Industry fit is assessed using an LLM, while interaction recency is calculated using the evaluation date.

## 3. Company Size Rating — 30%

Company size indicates the potential scale of an organization.

| Number of Employees | Rating |
| ------------------- | -----: |
| 501–5,000           |     10 |
| More than 5,000     |      9 |
| 51–500              |      8 |
| 11–50               |      6 |
| 1–10                |      4 |
| Missing or invalid  | Review |

Larger organizations receive higher ratings because they may represent greater opportunities for workflow automation solutions.

## 4. Industry Fit Rating — 25%

Industry fit evaluates how relevant the company's industry is to the workflow automation product.

This dimension is assessed using the NVIDIA Nemotron model.

| Rating | Interpretation                                     |
| ------ | -------------------------------------------------- |
| 10     | Strong fit supported by specific industry evidence |
| 7      | Plausible industry use cases                       |
| 5      | Unclear, mixed, or insufficient evidence           |
| 3      | Limited fit                                        |

The LLM receives lead and company context and returns a structured assessment containing:

- Industry rating
- Reasoning
- Confidence
- Needs-review indicator

When industry context is missing or insufficient, the assessment should remain conservative and may require manual review.

The LLM is not allowed to invent company-specific facts or unsupported business capabilities.

## 5. Lead Source Intent Rating — 30%

Lead source indicates the level of buying intent demonstrated by the acquisition channel.

| Lead Source             | Rating |
| ----------------------- | -----: |
| Inbound demo request    |     10 |
| Sales call              |      9 |
| Referral                |      8 |
| Webinar attendee        |      7 |
| Content download        |      5 |
| LinkedIn outreach       |      4 |
| Missing or unrecognized | Review |

Sources indicating direct interest in the product receive higher ratings than passive or outbound engagement.

## 6. Interaction Recency Rating — 15%

Recency measures how recently the lead interacted with the business.

It is calculated using the difference between the evaluation date and `last_interaction_date`.

| Days Since Interaction           | Rating |
| -------------------------------- | -----: |
| 0–7 days                         |     10 |
| 8–30 days                        |      8 |
| 31–90 days                       |      5 |
| 91–180 days                      |      3 |
| More than 180 days               |      1 |
| Missing, invalid, or future date | Review |

The evaluation date is configurable. If no evaluation date is provided, the pipeline uses the current system date.

This allows the same dataset to be evaluated at different points in time.

## 7. Weighted Score Calculation

The final lead score is calculated using a weighted average of the four dimensions.

Formula:

`Final Score = (Company Size × 0.30) + (Industry Fit × 0.25) + (Source Intent × 0.30) + (Recency × 0.15)`

Example:

Suppose a lead receives the following ratings:

| Dimension     | Rating | Weight | Weighted Contribution |
| ------------- | -----: | -----: | --------------------: |
| Company Size  |      8 |   0.30 |                  2.40 |
| Industry Fit  |      7 |   0.25 |                  1.75 |
| Source Intent |     10 |   0.30 |                  3.00 |
| Recency       |      8 |   0.15 |                  1.20 |
| **Total**     |        |        |              **8.35** |

The final score for this lead is **8.35 out of 10**.

## 8. Qualification Decision Thresholds

The weighted score is converted into a qualification decision.

| Final Score | Decision  |
| ----------- | --------- |
| 8.00–10.00  | Qualified |
| 5.00–7.99   | Review    |
| Below 5.00  | Rejected  |

### Decision Interpretation

- **Qualified:** The lead meets the qualification threshold and can proceed to outreach generation.
- **Review:** The lead requires further assessment or manual verification.
- **Rejected:** The lead does not meet the minimum qualification threshold.

## 9. Review Overrides

A high weighted score does not automatically guarantee qualification.

The system applies review overrides when critical information is missing or an assessment is uncertain.

A lead is assigned `review` when conditions such as the following occur:

- Required lead information is missing.
- Company size is missing or invalid.
- Lead source is missing or unrecognized.
- Interaction date is missing, invalid, or in the future.
- Industry assessment is unavailable or incomplete.
- The LLM returns `needs_review = True`.

These overrides prevent incomplete or uncertain records from being automatically qualified or rejected.

## 10. Priority Ranking

Qualified leads are ranked in descending order of their final weighted scores.

The highest-scoring qualified lead receives the highest priority.

This ranking helps sales teams focus on leads with stronger qualification signals first.

## 11. Design Principles

The rubric follows these principles:

1. **Consistency:** Rule-based dimensions use predefined rating criteria.
2. **Transparency:** Each lead receives a score and supporting reasoning.
3. **Explainability:** The system records reasons for review decisions.
4. **Conservative assessment:** Missing or uncertain information should not be treated as a positive signal.
5. **Time awareness:** Recency is calculated relative to a configurable evaluation date.
6. **Controlled automation:** Only qualified leads proceed to automated outreach generation.

## 12. Conclusion

The qualification rubric combines deterministic business rules with LLM-based industry assessment.

This hybrid approach provides a structured and explainable method for prioritizing B2B leads while preserving a manual review path for incomplete or uncertain records.

# Autonomous Social-Video Automation Blueprint

## Objective

Produce one evidence-based, general-education 60-second vertical video each day; preserve original materials; maintain a verifiable production ledger; and publish only through the account and platform interfaces that are actually authenticated and officially supported.

## Operating architectures

| Approach | What it does | Tradeoffs | Cost | Setup complexity |
|---|---|---|---|---|
| **Current daily operating workflow** | Uses the protected Drive workspace, AI research and production controls, the authenticated target browser account, and a daily execution schedule. | Supports AI judgment and controlled publishing, but cannot use a missing provider login or an account that differs from the target account. | Uses the existing scheduled execution allocation. | Low; already active. |
| **Durable code-backed orchestration** | Stores the workflow, state ledger, research rules, and integration adapters in a private GitHub repository; runs schedule logic from a durable service only after each provider exposes an authorized API or session. | Scales better and allows cross-platform adapters, but requires official provider authentication and secure credentials for each external channel. | Depends on the selected hosting and provider plans. | Medium to high. |

The current daily operating workflow remains the active route. The durable orchestration design is maintained as a ready implementation asset, but it must not be activated against Facebook, Julius, Antigravity, Gemini Spark, or another provider until its account and official capability have been confirmed.

## Daily production pipeline

| Stage | Required input | Output | Completion gate |
|---|---|---|---|
| 1. Topic selection | Topic queue, credible institutional and research sources, relevant expert lecture/interview evidence | One narrow learning question and source ledger | No personal advice, diagnosis, or result promise |
| 2. Research review | At least two independent high-quality sources; expert videos treated as secondary context | Claim map with source URLs, dates, authors, and evidence limitations | Every material claim cross-checked |
| 3. Script | Approved claim map and editorial standard | 60-second script with a question-based hook, context, evidence, limitations, and educational disclaimer | Claims use calibrated language and fit the narration time budget |
| 4. Visual plan | Script and topic | 9:16 storyboard, source references, narration and accessibility plan | No image, text, or motion implies a diagnosis or promised outcome |
| 5. Media production | User-owned source video only when identity and ownership are clear; otherwise AI-generated educational visuals | Final vertical export, cover, caption, alt text, sources note | Technical validation of duration, geometry, audio, and rendering |
| 6. Publishing | Official authenticated target channel | Published URL or a precise pending/blocker record | Never publish through a mismatched account; never duplicate a draft or post |
| 7. Monitoring | Official history, public post URL, and state ledger | Published, pending, failed, or retryable status | A status change must be verified before it is recorded |

## Health-information safeguards

All content must follow `HEALTH_CONTENT_EDITORIAL_STANDARD.md`. The workflow must cite or link to authoritative sources; distinguish research association from treatment advice; avoid sensationalism and stigmatizing language; and include a concise general-education disclaimer. Expert YouTube videos can inform topic selection, but they cannot be the sole support for factual claims.[1] [2] [3]

## Face and voice policy

User-supplied footage may be used only after the workflow establishes that the subject is the user or that the user has documented permission to use the subject’s likeness and voice. The production ledger must record the source file ID, technical analysis, ownership/consent confirmation, and whether the output is original footage, edited footage, or AI-generated visualization. Do not create a synthetic impersonation of another person.

## Integration matrix

| Service | Confirmed role | Current state | Automated action allowed now |
|---|---|---|---|
| Drive workspace | Source-of-truth storage and state ledger | Authorized | Yes: asset and status management |
| GitHub | Private code and workflow-asset repository | Authenticated as `balajirajput96` | Yes: repository and versioned workflow assets |
| Target Instagram account | Primary publishing destination | Authenticated browser publication completed for `@balajirajput96` | Only through the authenticated official browser path and only after required external-publication confirmation |
| Instagram connector | Separate connected account `@bala.jirajput966` | Authorized but not target-aligned | No target publication; may only be used where account alignment is verified |
| Google Gemini | Research and multimodal processing | Enabled connector | Use only for supported generation and analysis; do not claim Spark scheduling until authenticated |
| Google Antigravity CLI | Development and local agent workspace | Official CLI available but not installed or authenticated in this environment | Prepare repository workspace; do not run agents until authentication and workspace trust are confirmed |
| Julius | Scheduled analysis and data refresh | Official scheduled-run capability exists, but the browser is not authenticated | No current configuration or schedule creation |
| Facebook | Secondary publishing destination | No connector and browser requires login | No current publishing or scheduling |

## State and retry model

Every candidate has a stable state record keyed by source Drive file ID, SHA-256 checksum, normalized filename, topic ID, draft ID, and published URL or post ID. A post cannot re-enter production when any prior record is `prepared`, `submitted`, `pending_confirmation`, or `published`. Failures are classified as `source_quality`, `research_quality`, `render`, `authentication`, `provider_control`, or `publication`. Only deterministic, non-publication failures may retry automatically; authentication and provider-control failures remain pending until the provider confirms availability.

## Repository layout

```text
health-reels-automation/
  README.md
  policy/
    HEALTH_CONTENT_EDITORIAL_STANDARD.md
    ZERO_TOUCH_REELS_OPERATING_POLICY.md
  docs/
    AUTONOMOUS_SOCIAL_VIDEO_AUTOMATION_BLUEPRINT.md
    INTEGRATION_AUDIT.md
  state/
    schema.md
  prompts/
    research.md
    script.md
    visual_plan.md
    publish.md
```

## References

[1]: [U.S. Department of Health and Human Services — Health Misinformation](https://www.hhs.gov/surgeongeneral/reports-and-publications/health-misinformation/index.html)
[2]: [World Health Organization — Infodemic](https://www.who.int/health-topics/infodemic)
[3]: [National Institute of Mental Health — Mental Health Information](https://www.nimh.nih.gov/health)
[4]: [Google Antigravity CLI Overview](https://antigravity.google/docs/cli/overview)
[5]: [Julius — Scheduled Runs](https://julius.ai/product/scheduled-runs)

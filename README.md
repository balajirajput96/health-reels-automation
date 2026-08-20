# Health Reels Automation

This private repository is the version-controlled policy, safety, validation, and audit layer for the daily health-education Reels workflow. It intentionally excludes credentials, browser sessions, Drive contents, raw private videos, tokens, passwords, and user data.

## Operating Model

The workflow is divided into two deliberate layers. The controlled daily production process performs AI judgment, source validation, media assembly, account verification, and official Instagram publishing safeguards. This repository performs deterministic checks that can be reproduced without social-account access.

| Layer | Responsibility | Explicit boundary |
|---|---|---|
| Controlled daily Reels operation | Content selection, medical-safety review, media generation, final account verification, official publishing, Drive records | One complete non-duplicate Reel at a time; public Share requires the configured approval boundary. |
| Repository maintenance | Ledger validation, policy/document checks, deterministic tests, workflow cadence checks, and non-secret run reports | Does not access browser sessions, social accounts, Drive, credentials, publishing controls, or media-generation services. |

## Repository Structure

- `automation/state_guard.py` — idempotency guard for source IDs, checksums, filenames, drafts, and post IDs.
- `automation/maintenance_manifest.json` — versioned declaration of required files, ledger stages, target-account boundary, and expected workflow cadence.
- `automation/health_check.py` — non-destructive manifest, ledger, and workflow validation that writes JSON and Markdown run reports.
- `state/reels_ledger.json` — machine-readable state used to reject duplicate processing or publication.
- `policy/`, `standards/`, and `docs/` — approved operating and content-safety documents.
- `records/` — committed metadata, manifest, and publication evidence without raw media or secrets.
- `tests/` — deterministic unit tests for automation safeguards.

## Local Validation

Run the following from the repository root:

```bash
python -m unittest discover -s tests -v
python automation/state_guard.py status
python automation/health_check.py \
  --report-json /tmp/health-reels-health-check.json \
  --summary-md /tmp/health-reels-health-check.md
```

The health check reads repository files and writes only the requested report artifacts. A successful result means the required repository files, ledger structure, target-account boundary, published-post identifiers, and expected workflow schedules are internally consistent. It does not prove that an external account, browser session, API, Drive workspace, or publishing action is available.

## GitHub Actions

- **Daily Automation Audit** runs deterministic unit tests, validates the idempotency ledger, executes the manifest-driven health check, and uploads its JSON/Markdown result as a short-lived workflow artifact.
- **Daily Repository Maintenance** checks policy and documentation drift. Draft pull-request creation is disabled for scheduled runs and can be requested only through an explicit manual workflow input, subject to repository policy.

## Safety and Credential Boundary

Never commit, log, paste, or copy credentials into this repository. Do not use repository workflows to publish Reels, access browser cookies, handle Google or Instagram login, alter schedules, mutate Drive records, or bypass repository or platform controls. Any external action remains subject to the relevant official workflow and its approval boundary.

## Recovery Principle

Before a significant change, preserve recoverability through a branch, commit, test result, or artifact. Reuse validated existing scripts and prior commits where possible; do not reset repositories, delete historical records, or overwrite production assets during maintenance.

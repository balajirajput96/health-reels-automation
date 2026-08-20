# CLI Continuity Record

**Date:** 2026-08-20

## Purpose

This record preserves the non-secret operating knowledge required to continue the authorized health-Reels automation without exporting passwords, API keys, tokens, cookies, browser profiles, or session material.

## Declared Service Continuity

| Service | Recorded role | Authentication boundary | Current continuity state |
|---|---|---|---|
| Google Anti-gravity CLI | Supported Google AI command-line route for approved tasks | Official local credential store only | Command present; authenticated read-only capability was previously verified. |
| Google Jules | Browser-based coding-agent workspace | Official browser session only | Browser-authenticated workspace; no standalone local command detected. |
| Gemini CLI | Installed legacy client | Official local credential store only | Installed, but provider reports the individual route as unsupported; use Anti-gravity instead. |
| GitHub CLI | Private repository and Actions automation | Official GitHub CLI credential store only | Command present; active authorized repository access previously verified. |
| Google Workspace CLI | Protected Drive operational-record synchronization | Official local credential store only | Command present; use only for approved Drive actions. |

## Reusable Work Sources

The continuity layer uses the private Git repository, GitHub Actions run records, protected Drive operational records, reusable Reels scripts, safety standards, policy documents, and sanitized run summaries. It does not depend on raw shell-history files.

At the time of this record, the environment contained reusable Reels scripts and repository workflows, plus terminal output captures. The captures are not copied into GitHub because raw command output may include sensitive or personal material. Their useful knowledge is represented by committed scripts, manifests, tested checks, and selected sanitized records instead.

## Daily Automation Boundary

The existing daily Reels operation remains responsible for AI judgment, browser-dependent account verification, content production, protected Drive synchronization, and official publishing safeguards. The repository workflow performs deterministic validation only. It does not attempt to use browser sessions, invoke authenticated external CLIs, publish content, copy credentials, or change schedules.

## Non-Negotiable Guards

- Publish only to `@balajirajput96`; never publish to `@bala.jirajput966`.
- Do not mass-release content or upload incomplete Reel segments.
- Do not export, commit, print, or reconstruct secrets or sessions.
- Do not bypass login, MFA, CAPTCHA, provider restrictions, GitHub permissions, or platform policy.
- Record real provider and permission blockers accurately.

## Verification

The daily repository audit validates `automation/cli_continuity_manifest.json` and publishes a non-secret JSON/Markdown continuity artifact together with the existing repository health-check artifact.

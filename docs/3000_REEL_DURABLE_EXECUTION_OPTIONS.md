# Durable Execution Boundary for the 3,000 Hindi Research-Reel Pipeline

## Current verified state

The default work environment successfully produced and locally quality-checked a 54-second 1080×1920 Reel 0005 package, but it is not suitable for a persistent 3,000-item renderer because it can hibernate between sessions. The package is also blocked from upload by a canonical Drive identity collision; persistence does not override that evidence gate.

The long-running system must retain: source records, scripts, asset hashes, render/QC results, canonical Drive file IDs and checksums, retry reasons, and immutable transition events. It must never infer completion from a local file alone.

## User-facing durable options

| Approach | What it provides | Tradeoffs | Cost | Setup complexity |
|---|---|---|---|---|
| Managed production tracker and scheduled coordinator | A browser-accessible queue for evidence, scripts, retries, QC, Drive receipts, and production status. It can coordinate low-cost deterministic checks. | Managed hosting cannot run arbitrary system-level FFmpeg tooling or retain a specialized media CLI stack. It needs a separate renderer for final MP4 production. | Free to start; usage-based at higher scale. | Moderate. |
| User-owned connected renderer | The same verified queue and FFmpeg workflow run on existing hardware, with no additional server cost. | The machine must remain online and have enough storage; long jobs stop if the machine is offline. Google Drive access must use legitimate user-authorized OAuth, never copied connector credentials. | No additional hosting cost. | Moderate. |
| Independent persistent Linux renderer | A continuously available Linux worker can use FFmpeg, custom packages, persistent storage, system-level service recovery, and a durable retry queue. It directly supports batch transcoding and render/QC automation. | Paid infrastructure, operational monitoring, and legitimate Drive OAuth setup are required. It must be configured to restart safely and must not expose unauthenticated services. | Basic starts at **$10/month** (2 vCPU, 1 GB RAM, 35 GB storage). A 4-GB/70-GB tier is **$30/month** and is more suitable if concurrency or local working storage grows. Outbound traffic and storage overages may apply. | Moderate. |

## Hard requirements and safe boundary

The intended media workflow needs FFmpeg/FFprobe, subtitle fonts, generated media files, hash checks, local render logs, and a durable worker process. These are concrete operating-system-level requirements that the managed tracker alone cannot satisfy. A persistent Linux renderer or a connected personal computer is therefore required for unattended batch rendering.

No paid server, persistent worker, new OAuth credential, background job, or external deployment has been created. The active authenticated Drive connector remains task-local and must not be copied into another runtime. Any future worker must obtain its own legitimate authorization and save only non-secret identifiers and receipts.

## Required decision before unattended scale-out

Before starting persistent batch production beyond current-session work, select one of the three approaches above. The selected route must then be configured with a canonical collision check before every upload, bounded retries, an append-only transition log, and a stop condition for ambiguous Drive identities.

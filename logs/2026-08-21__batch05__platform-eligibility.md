# Batch 05 — Platform Eligibility Check

**Checked:** 2026-08-21, Asia/Kolkata release window.

| Platform | Verified finding | Staging decision |
|---|---|---|
| Instagram | The authenticated official browser session displayed `@balajirajput96`; the Batch 01 manifest identifies Batch 05 as the earliest complete validated unpublished final. The prior Batch 04 release is older than the same-day cadence boundary. | Eligible for official Instagram staging only. |
| Facebook | The official Facebook browser session is authenticated as Balaji Rajput. No independently verified official cross-post setting or linked target route for `@balajirajput96` was exposed during the eligibility check. | Do not stage or submit Facebook distribution in this run. Record as an accurate cross-post verification blocker rather than assuming a connection. |

No public Share action was taken during this check.

## Official Instagram staging progress

- The Batch 05 complete 60-second final video was attached through the official Instagram post dialog.
- The validated portrait crop was retained and the dialog advanced to the Edit stage.
- Instagram exposed one separate file input for the cover selector. Attempts to alter the dynamically generated input's DOM attributes through the page console encountered browser-level syntax/serialization errors. No cover file, caption, disclosure, scheduling setting, or public Share action was changed by those failed control-addressing attempts.
- The next supported interaction will retain the source-derived cover requirement and continue only if the official control can be addressed safely.

## Browser service blocker

At the official Instagram Edit stage, before entering the caption or taking any public Share action, the browser service returned a crash-loop protection error with a ten-minute retry interval. The Batch 05 final video had already been attached and the portrait crop retained, but the source-derived cover had not been confirmed as applied. The current Instagram editor state must therefore be treated as **staging incomplete**. No public distribution occurred on Instagram or Facebook.

## Recovered staging state

After the browser retry interval, the official Instagram editor preserved the attached Batch 05 video. The source-derived Batch 05 cover image was then successfully attached through Instagram's separate official cover selector. The editor remains at the non-public Edit stage with caption, AI-content disclosure, scheduling, and Share controls not yet changed.

## Details-stage control audit

The official Instagram New reel details screen is open for @balajirajput96. The source-derived cover has been selected. The visible controls show no added people, no collaborator selection, and the Schedule content control is off. The required AI-generated-content disclosure control is visible and currently off. The public Share control is visible but has not been activated. Caption entry remains pending.

## Caption and disclosure preparation

The approved Batch 05 caption, disclaimer, cited sources, and eight approved hashtags were entered once in Instagram's official caption field. Instagram displayed the caption at 618 of 2,200 characters. Its required `AI label` / `Add AI label` control is present in the official details pane and remains to be enabled. No tags, collaborators, schedule, or Share action has been selected.

## Staging preservation check

A keyboard action surfaced Instagram's `Discard post?` confirmation rather than changing publication settings. The prompt was explicitly cancelled, preserving the staged video and approved caption. The post was not discarded and no public Share action was taken. The details pane continues to expose the required `Add AI label` switch and the off Schedule content switch.

## Final pre-share audit

The Batch 05 Reel remains staged in the official Instagram dialog for the intended authenticated account, @balajirajput96. The source-derived cover is selected. The approved caption content, disclaimer, sources, and eight hashtags are present; Instagram’s editor normalizes intended paragraph separators as four internal line-break characters, with no additional words or tags. The AI-content label switch is enabled (`true`), while Schedule content is disabled (`false`). No people, collaborators, or Facebook distribution have been selected. The visible public Share control has not been activated.

## Publication confirmation and independent live verification

Instagram returned the explicit confirmation: `Your reel has been shared.` The independently loaded public Reels grid for @balajirajput96 then displayed the new first thumbnail, matching the Batch 05 source cover visual (person with coffee at a table and clock). Its independently identified public URL is:

https://www.instagram.com/balajirajput96/reel/DcUX5rJzI2g/

At verification time, the public grid showed an initial view count of 0. This confirmation applies only to Instagram; Facebook distribution was not attempted.

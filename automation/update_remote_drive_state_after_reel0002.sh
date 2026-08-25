#!/usr/bin/env bash
set -euo pipefail

PACKAGE="/home/ubuntu/repositories/health-reels-automation/production/active_drive_batch001/REEL-0002_habit_21_days"

gws drive files update --params '{"fileId":"1JPD_ArFxDCWxU5GCEq3DEiS9XT1ezeaE"}' --json '{"name":"checkpoint.json","mimeType":"application/json"}' --upload "$PACKAGE/remote_checkpoint_after_reel0002.json" --upload-content-type application/json --format json > "$PACKAGE/remote_update_checkpoint_result.json"
gws drive files update --params '{"fileId":"14kGl96jM4Lsd9xNgQaqxrrLPPCcAJLCj"}' --json '{"name":"reel_registry_3000_slots.json","mimeType":"application/json"}' --upload "$PACKAGE/remote_registry_after_reel0002.json" --upload-content-type application/json --format json > "$PACKAGE/remote_update_registry_result.json"
gws drive files update --params '{"fileId":"1SrrMU5Zh-GO9tDFJZfHvtVrbESO6rUNV"}' --json '{"name":"canonical_production_state.json","mimeType":"application/json"}' --upload "$PACKAGE/remote_canonical_production_state_after_reel0002.json" --upload-content-type application/json --format json > "$PACKAGE/remote_update_canonical_result.json"

printf 'remote_state_update_complete\n'

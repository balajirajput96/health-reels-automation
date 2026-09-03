#!/usr/bin/env python3
"""Resource Attribution Enforcement.

Enforces rules from enforcing-resource-attribution skill:
- BigQuery CLI (`bq`): Appends mandatory `--label datacloud=<ide>` (e.g. `datacloud=antigravity`).
- Google Cloud SDK (`gcloud`): Injects `CLOUDSDK_METRICS_ENVIRONMENT=datacloud.<ide>` (e.g. `CLOUDSDK_METRICS_ENVIRONMENT=datacloud.antigravity`).
"""

from __future__ import annotations
import os
import re
from typing import Sequence

DEFAULT_IDE = "antigravity"

def format_bq_command(cmd: Sequence[str] | str, ide: str = DEFAULT_IDE) -> list[str]:
    """Ensures BigQuery command includes mandatory --label datacloud=<ide>."""
    label_arg = f"datacloud={ide}"
    if isinstance(cmd, str):
        import shlex
        tokens = shlex.split(cmd)
    else:
        tokens = list(cmd)

    if not tokens or tokens[0] != "bq":
        return tokens

    # Check if --label is already present
    has_label = False
    for i, t in enumerate(tokens):
        if t == "--label" and i + 1 < len(tokens):
            has_label = True
            break
        elif t.startswith("--label="):
            has_label = True
            break

    if not has_label:
        # Insert after subcommand (e.g. 'bq query' -> 'bq query --label datacloud=antigravity')
        if len(tokens) > 1 and tokens[1] in ("query", "load", "extract", "mk", "cp"):
            tokens.insert(2, f"--label={label_arg}")
        else:
            tokens.append(f"--label={label_arg}")

    return tokens

def format_gcloud_env(existing_env: dict | None = None, ide: str = DEFAULT_IDE) -> dict:
    """Injects CLOUDSDK_METRICS_ENVIRONMENT=datacloud.<ide> into environment variables."""
    env = dict(existing_env or os.environ)
    env["CLOUDSDK_METRICS_ENVIRONMENT"] = f"datacloud.{ide}"
    return env

def wrap_gcloud_command_string(cmd_str: str, ide: str = DEFAULT_IDE) -> str:
    """Prepends CLOUDSDK_METRICS_ENVIRONMENT=datacloud.<ide> to a bash command string."""
    env_var = f"CLOUDSDK_METRICS_ENVIRONMENT=datacloud.{ide}"
    if env_var in cmd_str:
        return cmd_str
    return f"{env_var} {cmd_str}"

if __name__ == "__main__":
    import json
    demo_bq = format_bq_command(["bq", "query", "--use_legacy_sql=false", "SELECT 1"])
    demo_gcloud = wrap_gcloud_command_string("gcloud compute instances list")
    print(json.dumps({
        "attributed_bq": demo_bq,
        "attributed_gcloud": demo_gcloud,
    }, indent=2))

---
workspace_kind: research
contract_version: 1
project_id: "hpc-enabled"
local:
  experiment_root: "experiments"
  source_roots: ["src", "configs", "scripts"]
paper: null
hpc:
  host: "approved-host"
  project_root: "/remote/project"
sync:
  upload_allow: ["src/", "configs/", "scripts/"]
  upload_exclude: [".git/", "paper/", "runs/", "results/", "checkpoints/"]
  return_allow: ["runs/EXP-ID/metrics/", "reports/"]
---

# HPC-enabled fixture

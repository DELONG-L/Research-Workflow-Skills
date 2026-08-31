---
workspace_kind: research
contract_version: 1
project_id: "<project-id>"
local:
  experiment_root: "experiments"
  source_roots:
    - "src"
    - "configs"
    - "scripts"
paper:
  repository: "paper"
  link_file: ".research-workspace.yml"
  figure_manifest: "figure-manifest.yml"
hpc:
  host: "hpc"
  project_root: "$HOME/projects/<project-id>"
sync:
  upload_allow:
    - "src/"
    - "configs/"
    - "scripts/"
  upload_exclude:
    - ".git/"
    - "paper/"
    - "runs/"
    - "results/"
    - "checkpoints/"
    - "__pycache__/"
    - ".pytest_cache/"
    - "artifacts/paper/"
  return_allow:
    - "runs/<exp-id>/metrics/"
    - "runs/<exp-id>/MANIFEST.md"
    - "runs/<exp-id>/command.sh"
    - "reports/"
---

# Project Workspace

## Scope

- Local project root: `.`
- Primary research repository: this directory
- Paper repository: `paper/` (separate Git repository and Overleaf remote)
- Remote execution mirror: `$HOME/projects/<project-id>/`

## Local rules

- Keep raw data, checkpoints, full logs, and large intermediate artifacts out
  of the paper repository.
- Add `paper/` to the primary repository's `.gitignore` so the independent
  paper repository is not accidentally committed as an embedded repository.
- Keep project-wide planning at the root and experiment records under
  `experiments/EXP-*/`.
- Promote only final lightweight paper assets into `paper/`; record their
  provenance in `paper/figure-manifest.yml`.

## Change notes

- Record intentional changes to repository boundaries, remote roots, sync
  rules, or retention policy in this section or the project's existing notes.

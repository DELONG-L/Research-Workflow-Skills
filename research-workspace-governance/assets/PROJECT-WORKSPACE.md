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
paper: null
hpc: null
sync: null
---

# Project Workspace

## Scope

- Local project root: `.`
- Primary research repository: this directory
- Paper repository: not configured
- Remote execution mirror: not configured

## Local rules

- Keep project-wide planning at the root and experiment records under
  `experiments/EXP-*/`.
- Keep raw data immutable when required by the experiment record and separate
  derived data from its sources.

## Optional extensions

- Replace `paper: null` with a configured paper mapping only when the project
  has a separate paper Git repository. Add its path to the primary repository's
  `.gitignore`, create its explicit parent-contract link, and keep raw data,
  checkpoints, and full logs out of it.
- Replace both `hpc: null` and `sync: null` with project-approved mappings only
  when the project uses a remote execution mirror. Keep the local repository
  canonical and allow only declared upload and return paths.

## Change notes

- Record intentional changes to repository boundaries, remote roots, sync
  rules, or retention policy in this section or the project's existing notes.

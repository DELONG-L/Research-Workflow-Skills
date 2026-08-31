# Project Workspace Contract

## Purpose

`PROJECT-WORKSPACE.md` makes research-workspace rules opt-in at one project
root. It is a human-readable contract with small YAML front matter that tools
can recognize. The base contract governs the local repository. Paper and HPC
extensions are optional. The contract does not apply outside its root or across
another Git repository unless that repository has an explicit link.

## Discovery and scope

- Resolve from the user-selected target path, not from a general working
  directory.
- Accept a root contract only when `workspace_kind: research` is present in
  YAML front matter.
- A root contract applies to normal descendant directories.
- Stop automatic ancestor lookup at a Git repository boundary. When a separate
  paper repository is configured, it uses `.research-workspace.yml` to name its
  parent contract explicitly.
- If no contract is found, ordinary mode applies. Never infer managed status
  solely from words such as "paper", "experiment", or "research".

## Root contract fields

Use [PROJECT-WORKSPACE.md](../assets/PROJECT-WORKSPACE.md) as the starting
template. Keep paths relative to the local project root unless a field is
explicitly remote.

| Field | Required | Meaning |
| --- | --- | --- |
| `workspace_kind` | yes | Must be `research`. |
| `contract_version` | yes | Contract schema version, initially `1`. |
| `project_id` | yes | Stable identifier used by local records and optional extensions. |
| `local.experiment_root` | yes | Root for `EXP-*` records. |
| `local.source_roots` | yes | Version-controlled source/config/script roots. |
| `paper` | no | `null` or a configured paper-repository mapping. |
| `paper.repository` | yes when paper is configured | Relative path to the independent paper Git repository. |
| `paper.link_file` | yes when paper is configured | Link-file name inside that repository. |
| `paper.figure_manifest` | yes when paper is configured | Provenance manifest path inside the paper repository. |
| `hpc` | no | `null` or a configured execution-mirror mapping. |
| `hpc.host` | yes when HPC is configured | SSH alias or host approved for this project. |
| `hpc.project_root` | yes when HPC is configured | Remote execution-mirror directory. |
| `sync` | yes when HPC is configured | Upload, exclusion, and return policy. |
| `sync.upload_allow` | yes when HPC is used | Paths eligible for local-to-HPC upload. |
| `sync.upload_exclude` | yes when HPC is used | Paths that must stay out of normal upload. |
| `sync.return_allow` | yes when HPC is used | Lightweight paths eligible to return locally. |

An absent or `null` optional section means that extension is disabled, not
malformed. Do not silently repair an absent or conflicting required field. Ask
the user when a change affects a project identifier, repository boundary,
remote location, or data-retention decision.

## Standard topology

The local-only topology is sufficient:

```text
<project>/                         # canonical local research repository
  PROJECT-WORKSPACE.md             # opt-in root contract
  task_plan.md  notes.md           # optional program-level planning
  experiments/EXP-.../             # experiment records and manifests
  src/  configs/  scripts/
  data/                             # manifests/pointers; raw data may be external
```

When the paper extension is configured, add a separate repository:

```text
<project>/
  artifacts/paper/                 # promotable lightweight exports/provenance
  paper/                            # independent paper Git repository
    .research-workspace.yml         # explicit parent-contract link
    main.tex  sections/  figures/  tables/  references.bib
    figure-manifest.yml
```

The primary research repository must not use a paper-only remote such as an
Overleaf Git remote. Add the configured paper path to the primary repository's
`.gitignore` so it is not accidentally committed as an embedded repository;
use a Git submodule only after an explicit team decision.

## Optional extension examples

To enable a separate paper repository, replace `paper: null` with:

```yaml
paper:
  repository: "paper"
  link_file: ".research-workspace.yml"
  figure_manifest: "figure-manifest.yml"
```

To enable an HPC execution mirror, replace `hpc: null` and `sync: null` with
project-approved values:

```yaml
hpc:
  host: "<ssh-alias-or-host>"
  project_root: "<remote-project-root>"
sync:
  upload_allow: ["src/", "configs/", "scripts/"]
  upload_exclude: [".git/", "paper/", "runs/", "results/", "checkpoints/"]
  return_allow: ["runs/<exp-id>/metrics/", "reports/"]
```

## HPC boundary

This section applies only when both `hpc` and `sync` are configured. The local
repository remains canonical. The remote directory is an execution mirror and
heavy-artifact store, normally containing `src/`, `configs/`, `scripts/`,
`runs/`, and `reports/`.

Normal upload excludes at least `.git/`, `paper/`, `runs/`, `results/`,
`checkpoints/`, caches, local data not explicitly approved, and generated
paper exports. Normal return is limited to manifests, metrics, reports,
critical log excerpts, and deliberately promoted figures/tables. When an HPC
integration Skill is available, apply its size, authorization, and retention
rules as well; otherwise stop before ungoverned remote mutation.

## Paper link

This section applies only when `paper` is configured. Create the declared link
file from [paper-workspace-link.yml](../assets/paper-workspace-link.yml). Its
`parent_contract` is relative to the link file, normally
`../PROJECT-WORKSPACE.md`. Do not scan past the paper Git boundary when this
link is absent or invalid.

## Paper-asset provenance

This section applies only when `paper` is configured. Maintain the declared
figure manifest for each final figure or table promoted into the paper
repository. Each record should identify:

```yaml
artifact_id: "fig-main-result"
paper_path: "figures/main-result.pdf"
experiment_id: "EXP-2026-001"
run_id: "run-0042" # or data_snapshot when no executable run exists
source_data: "../artifacts/paper/main-result/source.csv"
generator: "scripts/plot_main_result.py"
code_revision: "<git-commit>"
status: "approved"
```

This provenance belongs in the manifest, experiment record, or project notes,
not in the paper body. Keep raw data, logs, checkpoints, and analysis scratch
files outside the paper repository.

## Audit invariants

Report, then repair with authorization, any of the following:

- missing or invalid root contract;
- experiment records outside the declared experiment root;
- when paper is configured, a paper repository without its explicit link or
  asset manifest;
- a paper-only remote such as Overleaf Git on the primary research repository;
- when HPC is configured, a missing sync policy or normal sync that includes
  the paper repository or generated/heavy paths;
- when paper is configured, paper assets without source, experiment/data,
  generator, or revision links;
- an unexplained project-ID mismatch, or a remote-root mismatch when HPC is
  configured.

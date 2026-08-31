# Project Workspace Contract

## Purpose

`PROJECT-WORKSPACE.md` makes research-workspace rules opt-in at one project
root. It is a human-readable contract with small YAML front matter that tools
can recognize. It does not apply outside that root or across an embedded Git
repository unless that repository has the explicit paper link below.

## Discovery and scope

- Resolve from the user-selected target path, not from a general working
  directory.
- Accept a root contract only when `workspace_kind: research` is present in
  YAML front matter.
- A root contract applies to normal descendant directories.
- Stop automatic ancestor lookup at a Git repository boundary. A separate
  `paper/` repository uses `.research-workspace.yml` to name its parent
  contract explicitly.
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
| `project_id` | yes | Stable identifier used by records and remote execution. |
| `local.experiment_root` | yes | Root for `EXP-*` records. |
| `local.source_roots` | yes | Version-controlled source/config/script roots. |
| `paper.repository` | yes | Relative path to the independent paper Git repository. |
| `paper.link_file` | yes | Link-file name inside that repository. |
| `paper.figure_manifest` | yes | Provenance manifest path inside the paper repository. |
| `hpc.host` | optional | SSH alias or host approved for this project. |
| `hpc.project_root` | optional | Remote execution-mirror directory. |
| `sync.upload_allow` | yes when HPC is used | Paths eligible for local-to-HPC upload. |
| `sync.upload_exclude` | yes when HPC is used | Paths that must stay out of normal upload. |
| `sync.return_allow` | yes when HPC is used | Lightweight paths eligible to return locally. |

Do not silently repair an absent or conflicting field. Ask the user when it
changes a project identifier, repository boundary, remote location, or data
retention decision.

## Standard topology

```text
<project>/                         # local research repository
  PROJECT-WORKSPACE.md             # opt-in root contract
  task_plan.md  notes.md           # program-level planning
  experiments/EXP-.../             # experiment records and manifests
  src/  configs/  scripts/
  data/                             # manifests/pointers; raw data is external or ignored
  artifacts/paper/                 # promotable, lightweight exports and provenance
  paper/                            # independent Git repository; Overleaf remote
    .research-workspace.yml         # explicit parent-contract link
    main.tex  sections/  figures/  tables/  references.bib
    figure-manifest.yml
```

The paper repository must not be the primary research repository's Overleaf
remote. It contains manuscript sources and final lightweight assets only. Add
`paper/` to the primary repository's `.gitignore` so it is not accidentally
committed as an embedded repository; use a Git submodule only after an explicit
team decision.

## HPC boundary

The local repository is canonical. The remote directory is an execution
mirror and heavy-artifact store, normally containing `src/`, `configs/`,
`scripts/`, `runs/`, and `reports/`.

Normal upload excludes at least `.git/`, `paper/`, `runs/`, `results/`,
`checkpoints/`, caches, local data not explicitly approved, and generated
paper exports. Normal return is limited to manifests, metrics, reports,
critical log excerpts, and deliberately promoted figures/tables. Apply the
existing `hpc-access` size, authorization, and retention rules as well.

## Paper link

Create `paper/.research-workspace.yml` from
[paper-workspace-link.yml](../assets/paper-workspace-link.yml). Its
`parent_contract` is relative to the link file, normally
`../PROJECT-WORKSPACE.md`. Do not scan past the paper Git boundary when this
link is absent or invalid.

## Paper-asset provenance

Maintain `paper/figure-manifest.yml` for each final figure or table promoted
into the paper repository. Each record should identify:

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
- a paper repository without its explicit link or asset manifest;
- an Overleaf remote on the primary research repository;
- normal HPC sync that includes the paper repository or generated/heavy paths;
- paper assets without source, experiment/data, generator, or revision links;
- unexplained project-ID or remote-root mismatch.

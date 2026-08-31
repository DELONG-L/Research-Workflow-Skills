---
name: research-workspace-governance
description: Establish, audit, reorganize, and govern a project-scoped local research workspace with optional HPC synchronization and an optional separate paper Git repository. Use when a user asks to initialize or organize a research project directory, audit, clean, or archive a research workspace, configure local-to-HPC sync rules, connect or reorganize a paper repository such as Overleaf Git, or repair research-workspace provenance. Do not use for ordinary temporary work, research ideation, protocol design, or manuscript prose alone.
---

# Research Workspace Governance

Keep managed research projects reproducible without imposing their layout on
ordinary work. Read [project-workspace-contract.md](references/project-workspace-contract.md)
before creating, auditing, moving, syncing, or archiving a managed workspace.

## Resolve the mode first

Use the user's actual target path, never a generated chat workspace, a home
directory, or an unrelated current directory as a project root.

1. Look for `PROJECT-WORKSPACE.md` in the target directory and its ancestors.
   Accept it only when its YAML front matter contains `workspace_kind: research`.
2. Stop ancestor lookup at the nearest Git repository boundary. For an
   independent paper repository, instead read its root
   `.research-workspace.yml`, resolve `parent_contract` relative to that file,
   and validate the referenced research contract.
3. If neither marker resolves, use **ordinary mode**. Do not create a marker,
   enforce research layout, or add planning files merely because the request
   sounds academic.
4. Treat an explicit request to initialize, reorganize, audit, sync, clean, or
   archive a research workspace as authorization to use this skill before a
   marker exists. Confirm an unclear target root; copy the templates only when
   creation is within the requested scope.

## Operate the managed workspace

### Initialize or reorganize

Inspect the existing tree, repository boundaries, and Git state first. Use
[PROJECT-WORKSPACE.md](assets/PROJECT-WORKSPACE.md) as the local-first root
contract. Add the optional paper or HPC sections only after the user has
selected those locations. Use
[paper-workspace-link.yml](assets/paper-workspace-link.yml) as the paper
repository's `.research-workspace.yml` only when a separate paper repository is
configured.

Keep the local project repository canonical. When a paper repository is
configured, keep it as a separate Git repository with its own remote; Overleaf
Git is supported but not required. Never expose experiment data, runs, or HPC
artifacts to a paper remote. Do not move existing files, change remotes, or
delete/ignore data without an explicit, reviewed plan.

### Audit or clean

Report the contract state, missing required roots, repository boundaries,
configured sync paths, configured paper-asset provenance, and
untracked/generated artifacts. Give a move, cleanup, or archive plan before
making a destructive or broad change.
Never treat a stale cache, checkpoint, or duplicate file as disposable without
the user's authorization and the applicable experiment retention record.

### Configure or perform HPC synchronization

Operate remotely only when both `hpc` and `sync` are configured. Upload only the
declared code and configuration paths. Exclude any paper repository, Git
metadata, checkpoints, results, caches, and other generated artifacts unless
the contract and user both authorize an exception. Pull back only the declared
lightweight outputs. When `hpc-access` is available, defer actual SSH, rsync, or
remote changes to it and its authorization rules. Otherwise provide the bounded
handoff and stop before ungoverned remote mutation.

### Link paper evidence

Apply this section only when `paper` is configured. Put manuscript sources and
final lightweight exports only in the declared paper repository. Keep the
declared figure manifest there and map each promoted figure or table to its
experiment ID, run ID or data snapshot, generator, source path, and code
revision. Keep internal provenance out of manuscript prose unless the paper
itself requires it.

## Handoffs

- When `planning-with-files` is available and the program needs persistent
  planning, keep its program-level plans at the contract root.
- `experiment-design-management`: create `EXP-*` records under the declared
  experiment root and preserve provenance for promoted paper assets.
- When `hpc-access` is available and HPC is configured, use the declared remote
  project root and sync policy; keep the remote project an execution mirror.
- When paper Skills are available and a paper repository is configured, write
  manuscript material only there and honor the paper link and asset manifest.

Optional integrations are not prerequisites for local workspace governance. Do
not duplicate this contract inside another Skill. If a managed workspace is
malformed or a required field is absent, report the gap and ask for the smallest
decision needed to repair it. Do not treat an absent optional paper, HPC, or
sync section as an error.

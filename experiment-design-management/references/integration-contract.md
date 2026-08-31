# Integration Contract

## Own one layer each

- In a project with a valid `PROJECT-WORKSPACE.md`, treat that contract as the shared location, repository-boundary, HPC-sync, and paper-asset-provenance source of truth. Use `research-workspace-governance` only to initialize, audit, reorganize, sync, clean, archive, or repair that contract; do not require it for ordinary experimental reasoning.
- Use `experiment-design-management` for the experiment record, lifecycle, reproducibility boundary, and research-specific task mapping.
- Use `planning-with-files` for a multi-experiment program plan, long-lived notes, and cross-session progress. Keep its `task_plan.md` separate from the canonical per-experiment records.
- Use `grilling` only when the user wants a plan, decision, or experimental boundary stress-tested. Record resolved research terminology and decisions in the canonical experiment or program records.
- Research experiments keep execution state in their canonical records and do not need first-use tracker setup. For separate product-engineering work, follow the repository's existing tracker convention or ask the user which tracker to use.
- Use `paper-writing`, `paper-policy`, and `paper-figures-tables` after results are ready to communicate. They may read experiment records but must not silently alter frozen study plans or provenance.

## Resolve overlap

If a request spans a research program and one experiment, create or update the program plan first, then link its relevant milestone to the experiment record. If it is only a protocol or analysis-plan change, do not create a second program plan.

For a managed workspace, resolve the contract before choosing paths. Keep program plans at the project root, experiment records under the declared experiment root, local code canonical, the HPC directory as an execution mirror, and manuscript sources only in the separate declared paper repository. A nested paper Git repository must use its explicit `.research-workspace.yml` link; do not discover the parent contract by traversing its Git boundary.

Use `execution-spec.md` only when an authorized run needs a distinct operational handoff beyond the protocol. Record reusable-code dependencies in the design, protocol, or program plan and handle them through the project's ordinary engineering workflow or existing tracker. `hpc-access` starts only after the relevant experiment records are ready and the user explicitly authorizes remote work.

If a workflow asks to publish tickets, preregistrations, approvals, or external records, show the exact target and obtain explicit authorization before writing outside the local research repository.

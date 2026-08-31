# Integration Contract

## Own one layer each

- In a project with a valid `PROJECT-WORKSPACE.md`, treat that contract as the shared location and repository-boundary source of truth, plus the HPC-sync or paper-asset-provenance source only when those optional sections are configured. Use `research-workspace-governance` when available to initialize, audit, reorganize, sync, clean, archive, or repair that contract; do not require it for ordinary experimental reasoning.
- Use `experiment-design-management` for the experiment record, lifecycle, reproducibility boundary, and research-specific task mapping.
- Use `planning-with-files`, when available, for a multi-experiment program plan, long-lived notes, and cross-session progress. Otherwise follow the project's existing program-planning convention. Keep program plans separate from canonical per-experiment records.
- Use `grilling`, when available, only when the user wants a plan, decision, or experimental boundary stress-tested. Otherwise perform the requested stress test directly. Record resolved research terminology and decisions in the canonical experiment or program records.
- Research experiments keep execution state in their canonical records and do not need first-use tracker setup. For separate product-engineering work, follow the repository's existing tracker convention or ask the user which tracker to use.
- Use paper Skills, when available, after results are ready to communicate. They may read experiment records but must not silently alter frozen study plans or provenance. Without them, leave a bounded communication handoff rather than treating the missing integration as a blocker.

A missing optional integration is not a reason to expand scope or abandon the
owned layer. Complete the local record work, state the handoff requirement, and
stop before any external or remote action that lacks an authorized workflow.

## Resolve overlap

If a request spans a research program and one experiment, create or update the program plan first, then link its relevant milestone to the experiment record. If it is only a protocol or analysis-plan change, do not create a second program plan.

For a managed workspace, resolve the contract before choosing paths. Keep
program plans at the project root, experiment records under the declared
experiment root, and local code canonical. When HPC is configured, keep the
remote directory as an execution mirror. When a paper repository is configured,
keep manuscript sources only there; a nested paper Git repository must use its
explicit `.research-workspace.yml` link rather than parent discovery across a
Git boundary.

Use `execution-spec.md` only when an authorized run needs a distinct operational
handoff beyond the protocol. Record reusable-code dependencies in the design,
protocol, or program plan and handle them through the project's ordinary
engineering workflow or existing tracker. An HPC integration, when available,
starts only after the relevant experiment records are ready and the user
explicitly authorizes remote work.

If a workflow asks to publish tickets, preregistrations, approvals, or external records, show the exact target and obtain explicit authorization before writing outside the local research repository.

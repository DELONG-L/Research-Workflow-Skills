---
name: experiment-design-management
description: Design, document, preregister, coordinate, and close formal scientific experiments with reproducible protocols, analysis plans, execution tasks, provenance records, and deviation logs. Use when a researcher explicitly asks to design or manage an experiment, turn a research question into a protocol, prepare a preregistration or analysis plan, freeze an execution-ready study, or make an experiment reproducible. Do not use for open-ended idea discovery, brainstorming, literature exploration, or early feasibility discussion unless the user asks to formalize an experiment; also exclude manuscript prose, final statistical inference, regulated-study approval, and laboratory safety instructions.
---

# Experiment Design Management

Own the experiment lifecycle from a research question to an auditable record. Keep the investigator responsible for scientific judgment, ethics, safety, and approval decisions.

## Entry gate

Keep open-ended idea discovery, brainstorming, literature exploration, and early
feasibility discussion in ordinary exploratory reasoning. During that phase, do
not assign an experiment ID, create experiment files, freeze a design, or turn
ideas into tickets merely because the topic may later become an experiment.

Enter the managed lifecycle only when the user explicitly asks to design,
formalize, preregister, execute, coordinate, reproduce, or manage an experiment,
or confirms that an explored idea should now become a formal experiment. If the
request remains exploratory, answer it at the exploratory level and leave
formalization optional.

## First-use setup

0. If the user-selected project resolves a `PROJECT-WORKSPACE.md` with `workspace_kind: research`, read it before inspecting the repository. Use its `project_id`, experiment root, data boundaries, and any configured paper/HPC paths; do not create a contract merely because an experiment is being planned. If it is missing or malformed and the user asked for workspace setup or repair, use `research-workspace-governance` when available. Otherwise report the contract gap and ask only for the smallest path or boundary decision needed; do not block ordinary experiment design on an optional workspace integration.
1. Inspect the repository for an existing experiment registry, data-management plan, ethics requirements, and naming conventions.
2. Do not initialize a tracker or ticket directory for a research experiment by default. Keep execution state in the experiment's canonical records. If the user wants a separate product-engineering tracker, follow the repository's existing convention or ask which tracker to use.
3. If experimental terminology or design boundaries are ambiguous and the user wants them stress-tested, use `grilling` when available; otherwise stress-test the consequential decisions directly. Record resolved terminology and decisions in `design.md`; do not create a separate glossary or ADR workflow by default.
4. Propose an experiment identifier such as `EXP-2026-001`; do not create records or change a protocol until the researcher confirms the design boundary.

Use the contract's experiment root when a managed workspace applies; otherwise use `experiments/<experiment-id>/` by default in a research repository. In a projectless session, use `work/experiments/<experiment-id>/`. Read [experiment-records.md](references/experiment-records.md) before creating or revising an experiment record.

## Workflow

### 1. Establish the design

Resolve the research question, confirmatory and exploratory claims, target population or system, outcomes, factors, controls, unit of analysis, sampling or data-acquisition plan, bias controls, and stopping conditions. Record unknowns explicitly; never manufacture a power calculation, a preregistration status, ethical approval, or a feasibility claim.

For human, clinical, animal, hazardous, or privacy-sensitive work, capture the applicable approval, consent, safety, access, and retention requirements. Do not treat this skill as permission to conduct the work.

### 2. Freeze the record before execution

Create or update these versioned artifacts:

- `design.md` for rationale and design decisions;
- `protocol.md` for the executable procedure and quality checks;
- `analysis-plan.md` for confirmatory analysis, exclusions, transformations, missing-data handling, and exploratory boundaries;
- `data-manifest.yml` for inputs, outputs, code, environment, access, and checksums;
- optional `execution-spec.md` when remote, distributed, or multi-stage execution needs an operational bridge beyond the protocol;
- `deviations.md` for any change after the protocol or analysis plan is frozen.

Mark each artifact as `draft`, `reviewed`, `frozen`, or `superseded`, with an owner and date. Record version changes rather than silently replacing a frozen plan.

### 3. Turn the protocol into executable work

Derive execution work directly from the approved experiment records. For a
self-contained experiment, `protocol.md`, `analysis-plan.md`,
`data-manifest.yml`, and `execution-log.md` are sufficient; do not create a
separate specification or ticket set merely to satisfy a workflow.

Create `execution-spec.md` from
[execution-spec.md](assets/execution-spec.md) only when an operational handoff
is genuinely needed, such as remote HPC execution, multiple operators,
distributed stages, or a separately reviewed pilot-to-main transition. Trace
it to the frozen source-record versions and keep it operational rather than
turning it into a product specification.

Use `planning-with-files`, when available, only for program-level milestones
spanning multiple experiments or sessions. Otherwise follow the project's
existing program-planning convention. Handle reusable software or
infrastructure through the project's ordinary engineering workflow or existing
tracker when the user asks; do not require another Skill handoff. Use
`hpc-access` when available only after the relevant experiment records are ready
and the user authorizes remote work. Without it, prepare a bounded operational
handoff and stop before ungoverned remote mutation.

### 4. Preserve provenance during execution

Keep raw data immutable. Store derived data separately. Link every dataset, script or notebook, environment, instrument configuration, and result to the experiment ID and relevant protocol or analysis-plan version. Log deviations at the time they occur, including their likely impact on the confirmatory claim.

Do not relabel an exploratory result as confirmatory after inspecting it. If the research question changes materially, create a new experiment or explicitly supersede the original plan.

### 5. Close and hand off

Before reporting results, complete `results.md` with the design version,
data-freeze reference, analysis version, deviations, limitations, and
reproduction path. When paper Skills are available, hand manuscript prose and
submission-policy work to them. Otherwise keep the experiment record complete
and provide a bounded communication handoff; manuscript work never replaces or
silently changes the experiment record.

Read [integration-contract.md](references/integration-contract.md) when this skill overlaps with other planning, workspace, paper, or engineering skills.

## Output rules

- Prefer concrete, researcher-reviewable records over generic advice.
- Separate prespecified, confirmatory, secondary, and exploratory work.
- Ask for a decision when a design choice materially changes the inference; inspect local evidence before asking about facts discoverable in the project.
- Preserve identifiers and provenance links across every artifact.
- Do not create, submit, or modify external preregistrations, ethics applications, or issue-tracker records without explicit authorization.

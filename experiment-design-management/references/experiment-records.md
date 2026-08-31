# Experiment Records

Use one directory per experiment. Keep raw data outside the directory when required by storage or access policy, but reference it from the manifest.

```text
experiments/EXP-YYYY-NNN/
  design.md
  protocol.md
  analysis-plan.md
  data-manifest.yml
  execution-spec.md  # optional operational handoff
  execution-log.md
  deviations.md
  results.md
```

## `design.md`

```markdown
# EXP-YYYY-NNN — <title>

**Status:** draft | reviewed | frozen | superseded  
**Owner:** <name>  
**Last updated:** YYYY-MM-DD  
**Protocol version:** v0.x

## Research question and target claim
## Hypotheses
- Confirmatory:
- Exploratory:

## Design
- Study type and unit of analysis:
- Population/system and inclusion/exclusion criteria:
- Outcomes and measures:
- Factors, conditions, controls, and comparators:
- Sampling/data-acquisition plan and rationale:
- Randomization, blinding, or counterbalancing:
- Stopping rule:

## Risks and governance
- Ethics/safety/privacy status:
- Data management and access:

## Decisions and open questions
```

## `protocol.md`

```markdown
# Protocol — EXP-YYYY-NNN

**Status:** draft | reviewed | frozen | superseded  
**Version:** v0.x  
**Depends on:** <design version / approvals / materials or dataset version>

## Preconditions and materials
## Procedure
1. <action, record to capture, and quality check>

## Quality controls and failure handling
## Records produced
## Change control
Record every post-freeze change in `deviations.md` before proceeding when practical.
```

## `analysis-plan.md`

```markdown
# Analysis Plan — EXP-YYYY-NNN

**Status:** draft | reviewed | frozen | superseded  
**Version:** v0.x  
**Data-freeze criterion:** <condition>

## Confirmatory estimands and hypotheses
## Inclusion, exclusion, and missing-data rules
## Preprocessing and transformations
## Primary model or statistical procedure
## Multiplicity, uncertainty, and decision criteria
## Sensitivity and robustness analyses
## Exploratory analyses (clearly separated)
## Reporting plan and reproduction environment
```

## `execution-spec.md`

Create this optional operational bridge only when remote, distributed,
multi-stage, or multi-operator execution needs more detail than the protocol.
It names the source-record versions, inputs, code and environment, procedure,
quality gates, outputs, provenance, HPC handoff, and acceptance criteria. It
does not replace `protocol.md` or `analysis-plan.md`. Start from
[execution-spec.md](../assets/execution-spec.md).

## `data-manifest.yml`

```yaml
experiment_id: EXP-YYYY-NNN
protocol_version: v0.x
analysis_plan_version: v0.x
raw_data:
  - location: <approved immutable location>
    version: <identifier>
    checksum: <if available>
derived_data:
  - location: <location>
    generated_from: <raw-data identifier>
data_freeze:
  status: draft | frozen
  snapshot: <immutable derived-data or analysis-input identifier>
  source_runs: <run IDs or manifests>
  frozen_at: <timestamp>
code:
  repository: <URL or local path>
  revision: <commit or version>
environment: <lockfile, container, or environment identifier>
access: <owner and access constraints>
```

At data freeze, preserve the locked `raw_data` entry. Add a versioned
`data_freeze` entry or create the project's declared versioned manifest
successor; do not silently overwrite the source-data identity.

## `execution-log.md`

```markdown
# Execution Log — EXP-YYYY-NNN

| Timestamp | Run or batch ID | Operator | Input/data version | Protocol version | Configuration / seed | Output location | QC outcome |
| --- | --- | --- | --- | --- | --- | --- | --- |
```

Link an unexpected outcome to `deviations.md`; do not overwrite the original run record.

## `deviations.md`

```markdown
# Deviations — EXP-YYYY-NNN

| Date | Record/version affected | Deviation | Rationale | Expected impact | Approved by |
| --- | --- | --- | --- | --- | --- |
```

## `results.md`

```markdown
# Results — EXP-YYYY-NNN

**Design version:** v0.x  
**Protocol version:** v0.x  
**Analysis-plan version:** v0.x  
**Data freeze:** <manifest or dataset identifier>  
**Analysis revision/environment:** <identifier>

## Confirmatory results
## Secondary and exploratory results
## Deviations and their impact
## Limitations and scope of inference
## Reproduction path
```

# User guide

[Back to README](../README.md) · [简体中文](guide.zh-CN.md)

# Research Workflow Skills

Two open-source Codex Skills for governing reproducible research work:

- `experiment-design-management` formalizes and manages an experiment from
  design through closure.
- `research-workspace-governance` governs a local research repository with
  optional paper-repository and HPC extensions.

The Skills are complementary but independently installable. Workspace
governance owns paths and repository boundaries; experiment management owns
scientific records and lifecycle state. Neither Skill grants permission for
external submission, remote mutation, regulated work, or destructive cleanup.

[中文说明](../README.zh-CN.md)

## Install with Codex

In a Codex conversation with GitHub access, paste this request:

```text
Install both Codex Skills from this GitHub repository:

https://github.com/DELONG-L/Research-Workflow-Skills

Install these repository paths from the main branch:
- experiment-design-management
- research-workspace-governance

Do not overwrite an existing installation. After installation, validate both
Skills and tell me that they will be available from my next turn.
```

Providing the URL alone does not authorize installation. The request should
explicitly ask the agent to install the named Skill paths. Codex's Skill
installer aborts when a destination already exists and installs successful
downloads into the configured Codex Skill directory.

## Manual installation

Clone the repository using its canonical case-preserving URL:

```sh
git clone https://github.com/DELONG-L/Research-Workflow-Skills.git
cd Research-Workflow-Skills
```

Copy one or both Skill directories into your Codex Skill directory. Check for
existing installations first; do not merge over an installed copy.

```sh
skill_root="${CODEX_HOME:-$HOME/.codex}/skills"
test ! -e "$skill_root/experiment-design-management"
test ! -e "$skill_root/research-workspace-governance"
mkdir -p "$skill_root"
cp -R experiment-design-management "$skill_root/"
cp -R research-workspace-governance "$skill_root/"
```

To install only one Skill, run only its matching preflight and copy command.
Restart or refresh Codex after installation if it does not discover the Skill
immediately.

## Invoke

Both Skills allow normal automatic discovery. They can also be invoked
explicitly:

```text
Use $experiment-design-management to turn this approved research question
into a reproducible protocol and analysis plan.

Use $research-workspace-governance to initialize a local-only research
workspace in this repository.
```

Open-ended idea discovery does not activate the managed experiment lifecycle.
Ordinary directories do not become managed research workspaces unless a valid
contract exists or the user explicitly requests initialization or repair.

## Workspace modes

The base contract is local-only:

```text
project/
├── PROJECT-WORKSPACE.md
├── experiments/EXP-.../
├── src/
├── configs/
└── scripts/
```

A paper repository is an optional, separate Git repository linked explicitly
to the parent contract. Overleaf Git is supported but not required. HPC is
also optional: when configured, the local repository remains canonical and the
remote directory is only an execution mirror. See
[`project-workspace-contract.md`](../research-workspace-governance/references/project-workspace-contract.md)
for the conditional fields and examples.

## Validate

The validator uses Python 3 and PyYAML. It validates both Skill packages,
workspace contracts, UI metadata, links, evaluation corpora, private-path and
secret patterns, unit tests, and Git whitespace. When Codex's bundled
`quick_validate.py` is available, it runs that validator too.

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements-dev.txt
python scripts/validate_all.py
```

CI runs the same repository-level command.

## Versions

- Git tags describe repository releases, beginning with `v0.1.0`.
- `contract_version` describes the `PROJECT-WORKSPACE.md` schema and changes
  only when compatibility requires it.
- Hosted immutable Skill versions, if created later, are a separate delivery
  mechanism and do not replace Git release history.
- `SOURCE_SNAPSHOT.sha256` records the original imported source baseline; it
  is provenance evidence, not the checksum of the current release tree.

## Uninstall

Confirm the exact installation root, then remove only the corresponding
`experiment-design-management` and/or `research-workspace-governance`
directories. Removing a Skill does not remove research records the Skill
created inside your projects.

## License

[MIT](../LICENSE)

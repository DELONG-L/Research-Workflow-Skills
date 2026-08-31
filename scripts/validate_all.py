#!/usr/bin/env python3
"""Validate the repository's Skill packages and release contracts."""

import json
import os
import re
import subprocess
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILL_NAMES = (
    "experiment-design-management",
    "research-workspace-governance",
)
LINK_PATTERN = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
UNFINISHED_PATTERN = re.compile(r"\b(?:TODO|TBD|FIXME|REPLACE_ME)\b")
PRIVATE_PATTERNS = (
    re.compile(r"/Users/[^/<\s]+"),
    re.compile(r"/home/[^/<\s]+"),
    re.compile(r"BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY"),
    re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
)


class ValidationError(RuntimeError):
    """Raised when a release invariant is violated."""


def extract_front_matter(path):
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValidationError(f"{path}: missing opening YAML front matter")
    try:
        end = next(i for i, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration as exc:
        raise ValidationError(f"{path}: missing closing YAML front matter") from exc
    data = yaml.safe_load("\n".join(lines[1:end]))
    if not isinstance(data, dict):
        raise ValidationError(f"{path}: front matter must be a mapping")
    return data


def validate_skill(skill_dir):
    name = skill_dir.name
    metadata = extract_front_matter(skill_dir / "SKILL.md")
    if metadata.get("name") != name:
        raise ValidationError(f"{name}: front-matter name must match its directory")
    if not isinstance(metadata.get("description"), str) or not metadata["description"].strip():
        raise ValidationError(f"{name}: description is required")

    agent_path = skill_dir / "agents" / "openai.yaml"
    agent = yaml.safe_load(agent_path.read_text(encoding="utf-8"))
    interface = agent.get("interface") if isinstance(agent, dict) else None
    if not isinstance(interface, dict):
        raise ValidationError(f"{agent_path}: interface mapping is required")
    short = interface.get("short_description")
    if not isinstance(short, str) or not 25 <= len(short) <= 64:
        raise ValidationError(f"{agent_path}: short_description must be 25-64 characters")
    prompt = interface.get("default_prompt")
    if not isinstance(prompt, str) or f"${name}" not in prompt:
        raise ValidationError(f"{agent_path}: default_prompt must name ${name}")


def require_keys(mapping, keys, label):
    missing = [key for key in keys if key not in mapping]
    if missing:
        raise ValidationError(f"{label}: missing {', '.join(missing)}")


def validate_workspace_contract(data, label="contract"):
    require_keys(data, ("workspace_kind", "contract_version", "project_id", "local"), label)
    if data["workspace_kind"] != "research":
        raise ValidationError(f"{label}: workspace_kind must be research")
    if not isinstance(data["project_id"], str) or not data["project_id"].strip():
        raise ValidationError(f"{label}: project_id must be a non-empty string")
    local = data["local"]
    if not isinstance(local, dict):
        raise ValidationError(f"{label}: local must be a mapping")
    require_keys(local, ("experiment_root", "source_roots"), f"{label}.local")
    if not isinstance(local["source_roots"], list) or not local["source_roots"]:
        raise ValidationError(f"{label}.local.source_roots must be a non-empty list")

    paper = data.get("paper")
    if paper is not None:
        if not isinstance(paper, dict):
            raise ValidationError(f"{label}.paper must be null or a mapping")
        require_keys(paper, ("repository", "link_file", "figure_manifest"), f"{label}.paper")

    hpc = data.get("hpc")
    sync = data.get("sync")
    if hpc is None and sync is not None:
        raise ValidationError(f"{label}: sync requires hpc")
    if hpc is not None:
        if not isinstance(hpc, dict):
            raise ValidationError(f"{label}.hpc must be null or a mapping")
        require_keys(hpc, ("host", "project_root"), f"{label}.hpc")
        if not isinstance(sync, dict):
            raise ValidationError(f"{label}: configured hpc requires sync")
        require_keys(sync, ("upload_allow", "upload_exclude", "return_allow"), f"{label}.sync")
        for key in ("upload_allow", "upload_exclude", "return_allow"):
            if not isinstance(sync[key], list):
                raise ValidationError(f"{label}.sync.{key} must be a list")


def validate_internal_links(root=ROOT):
    errors = []
    for path in root.rglob("*.md"):
        if ".git" in path.parts:
            continue
        for target in LINK_PATTERN.findall(path.read_text(encoding="utf-8")):
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            clean = target.split("#", 1)[0]
            if clean and not (path.parent / clean).resolve().exists():
                errors.append(f"{path.relative_to(root)} -> {target}")
    if errors:
        raise ValidationError("broken relative links:\n" + "\n".join(errors))


def public_text_files(root=ROOT):
    suffixes = {".md", ".yml", ".yaml", ".json", ".py", ".txt"}
    for path in root.rglob("*"):
        if path.resolve() == Path(__file__).resolve():
            continue
        if path.is_file() and path.suffix in suffixes and ".git" not in path.parts:
            yield path


def validate_public_text(root=ROOT):
    for path in public_text_files(root):
        text = path.read_text(encoding="utf-8")
        if UNFINISHED_PATTERN.search(text):
            raise ValidationError(f"{path.relative_to(root)}: unfinished scaffold marker")
        for pattern in PRIVATE_PATTERNS:
            if pattern.search(text):
                raise ValidationError(f"{path.relative_to(root)}: private path or secret-like value")


def validate_eval_file(path):
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("version") != 1 or not isinstance(data.get("skill"), str):
        raise ValidationError(f"{path}: invalid evaluation header")
    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValidationError(f"{path}: at least one evaluation case is required")
    seen = set()
    for case in cases:
        if not isinstance(case, dict):
            raise ValidationError(f"{path}: each case must be a mapping")
        require_keys(case, ("id", "request", "expected", "forbidden"), str(path))
        if case["id"] in seen:
            raise ValidationError(f"{path}: duplicate case id {case['id']}")
        seen.add(case["id"])
        if not isinstance(case["expected"], list) or not case["expected"]:
            raise ValidationError(f"{path}: {case['id']} needs expected invariants")
        if not isinstance(case["forbidden"], list):
            raise ValidationError(f"{path}: {case['id']} forbidden must be a list")


def find_quick_validator():
    configured = os.environ.get("CODEX_QUICK_VALIDATE")
    candidates = [Path(configured).expanduser()] if configured else []
    candidates.extend(
        [
            Path.home() / ".codex/skills/.system/skill-creator/scripts/quick_validate.py",
            Path.home() / ".codex/skills/skill-creator/scripts/quick_validate.py",
        ]
    )
    return next((path for path in candidates if path.is_file()), None)


def run(command):
    subprocess.run(command, cwd=str(ROOT), check=True)


def main():
    for name in SKILL_NAMES:
        validate_skill(ROOT / name)
    template = extract_front_matter(
        ROOT / "research-workspace-governance/assets/PROJECT-WORKSPACE.md"
    )
    validate_workspace_contract(template, "base workspace template")
    validate_internal_links()
    validate_public_text()
    eval_paths = sorted(ROOT.glob("**/evals/*.json"))
    if len(eval_paths) != 3:
        raise ValidationError("expected exactly three evaluation corpora")
    for path in eval_paths:
        validate_eval_file(path)

    quick_validator = find_quick_validator()
    if quick_validator:
        for name in SKILL_NAMES:
            run([sys.executable, str(quick_validator), str(ROOT / name)])
    else:
        print("Codex quick_validate.py not found; repository checks remain active.")

    run([sys.executable, "-m", "compileall", "-q", "scripts", "tests"])
    run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"])
    if (ROOT / ".git").exists():
        run(["git", "diff", "--check"])
    print("All repository validations passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

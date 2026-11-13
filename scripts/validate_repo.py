#!/usr/bin/env python3
"""Validate the public structure and internal links of CN WorkDocs."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote

import yaml


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "cn-workdocs" / "SKILL.md"
OPENAI_YAML = ROOT / "skills" / "cn-workdocs" / "agents" / "openai.yaml"
REQUIRED_FILES = (
    ROOT / "README.md",
    ROOT / "LICENSE",
    ROOT / "CONTRIBUTING.md",
    ROOT / "SECURITY.md",
    SKILL,
    ROOT / "skills" / "cn-workdocs" / "agents" / "openai.yaml",
    ROOT / "skills" / "cn-workdocs" / "references" / "evidence-control.md",
    ROOT / "skills" / "cn-workdocs" / "references" / "document-types.md",
    ROOT / "skills" / "cn-workdocs" / "references" / "revision-and-tone.md",
    ROOT / "skills" / "cn-workdocs" / "references" / "delivery-and-qa.md",
    ROOT / "examples" / "pilot-proposal.md",
    ROOT / "examples" / "meeting-minutes.md",
    ROOT / "examples" / "audit-unsupported-claims.md",
)

LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
FRONTMATTER_RE = re.compile(r"\A---\n(?P<body>.*?)\n---\n", re.DOTALL)
PLACEHOLDERS = ("[TODO", "TODO:", "TBD:")


def markdown_files(root: Path) -> list[Path]:
    return sorted(path for path in root.rglob("*.md") if ".git" not in path.parts)


def yaml_files(root: Path) -> list[Path]:
    return sorted(
        path
        for pattern in ("*.yml", "*.yaml")
        for path in root.rglob(pattern)
        if ".git" not in path.parts
    )


def check_required_files(root: Path = ROOT) -> list[str]:
    files = REQUIRED_FILES if root == ROOT else tuple(root / path.relative_to(ROOT) for path in REQUIRED_FILES)
    return [f"missing required file: {path.relative_to(root)}" for path in files if not path.is_file()]


def check_skill_frontmatter(skill: Path = SKILL) -> list[str]:
    if not skill.is_file():
        return [f"missing skill entrypoint: {skill}"]
    text = skill.read_text(encoding="utf-8")
    match = FRONTMATTER_RE.match(text)
    if not match:
        return ["SKILL.md must start with YAML frontmatter"]
    try:
        body = yaml.safe_load(match.group("body"))
    except yaml.YAMLError as exc:
        return [f"SKILL.md has invalid YAML frontmatter: {exc}"]
    if not isinstance(body, dict):
        return ["SKILL.md frontmatter must be a mapping"]
    errors: list[str] = []
    if body.get("name") != "cn-workdocs":
        errors.append("SKILL.md name must be cn-workdocs")
    description = body.get("description")
    if not isinstance(description, str) or len(description.strip()) < 80:
        errors.append("SKILL.md needs a discriminating description")
    return errors


def check_yaml_files(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    for path in yaml_files(root):
        try:
            yaml.safe_load(path.read_text(encoding="utf-8"))
        except yaml.YAMLError as exc:
            errors.append(f"invalid YAML in {path.relative_to(root)}: {exc}")
    return errors


def check_openai_metadata(path: Path = OPENAI_YAML) -> list[str]:
    if not path.is_file():
        return [f"missing Codex interface metadata: {path}"]
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        return [f"invalid Codex interface metadata: {exc}"]
    interface = data.get("interface") if isinstance(data, dict) else None
    if not isinstance(interface, dict):
        return ["openai.yaml needs an interface mapping"]
    errors: list[str] = []
    if interface.get("display_name") != "CN WorkDocs":
        errors.append("openai.yaml display_name must be CN WorkDocs")
    description = interface.get("short_description")
    if not isinstance(description, str) or not 25 <= len(description) <= 64:
        errors.append("openai.yaml short_description must contain 25-64 characters")
    prompt = interface.get("default_prompt")
    if not isinstance(prompt, str) or "$cn-workdocs" not in prompt:
        errors.append("openai.yaml default_prompt must mention $cn-workdocs")
    return errors


def check_placeholders(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    for path in markdown_files(root):
        text = path.read_text(encoding="utf-8")
        for marker in PLACEHOLDERS:
            if marker in text:
                errors.append(f"unfinished scaffold marker {marker!r}: {path.relative_to(root)}")
    return errors


def check_links(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    resolved_root = root.resolve()
    for path in markdown_files(root):
        text = path.read_text(encoding="utf-8")
        for target in LINK_RE.findall(text):
            target = target.split("#", 1)[0].strip()
            if not target or target.startswith(("http://", "https://", "mailto:")):
                continue
            decoded = unquote(target)
            candidate = Path(decoded)
            if candidate.is_absolute() or re.match(r"^[A-Za-z]:[/\\]", decoded):
                errors.append(f"nonportable absolute link in {path.relative_to(root)}: {target}")
                continue
            resolved = (path.parent / candidate).resolve()
            try:
                resolved.relative_to(resolved_root)
            except ValueError:
                errors.append(f"link escapes repository in {path.relative_to(root)}: {target}")
                continue
            if not resolved.exists():
                errors.append(f"broken link in {path.relative_to(root)}: {target}")
    return errors


def validate(root: Path = ROOT) -> list[str]:
    return (
        check_required_files(root)
        + check_skill_frontmatter(root / SKILL.relative_to(ROOT))
        + check_yaml_files(root)
        + check_openai_metadata(root / OPENAI_YAML.relative_to(ROOT))
        + check_placeholders(root)
        + check_links(root)
    )


def main() -> int:
    errors = validate(ROOT)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(
        f"OK: validated {len(markdown_files(ROOT))} Markdown files, "
        f"{len(yaml_files(ROOT))} YAML files, and skill metadata"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

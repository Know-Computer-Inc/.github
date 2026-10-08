#!/usr/bin/env python3
"""Static validation for the Know-Computer-Inc/.github repository.

Runs in CI (see .github/workflows/ci.yml) and locally:

    python scripts/validate_repo.py

Checks, in order:
  1. required community and profile files exist;
  2. every YAML file parses;
  3. GitHub issue forms and issue config match the supported schema;
  4. workflow files: triggers, least-privilege permissions, SHA-pinned actions,
     no `pull_request_target`;
  5. workflow-templates metadata files are valid JSON with the required keys;
  6. relative links between Markdown files resolve;
  7. no credential-shaped strings are committed.

This is static validation. It does not prove that a workflow runs on GitHub,
that a branch protection rule exists, or that a reported control is enabled —
see docs/SECURITY_BASELINE.md for that distinction.

Requires: Python 3.10+ and PyYAML.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("PyYAML is required: python -m pip install pyyaml")

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FILES = [
    "README.md",
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "SUPPORT.md",
    "PULL_REQUEST_TEMPLATE.md",
    "profile/README.md",
    ".github/CODEOWNERS",
    ".github/dependabot.yml",
    "docs/ENGINEERING_PRINCIPLES.md",
    "docs/REPOSITORY_STANDARDS.md",
    "docs/SECURITY_BASELINE.md",
    "docs/AI_ENGINEERING_POLICY.md",
    "docs/GOVERNANCE.md",
    "docs/adr/README.md",
    "docs/adr/TEMPLATE.md",
]

ISSUE_FORM_TYPES = {"markdown", "textarea", "input", "dropdown", "checkboxes"}

# Files the secret scanner skips: the scanner itself, whose patterns are
# deliberately written as literals.
SECRET_SCAN_SKIP = {"scripts/validate_repo.py"}

# (compiled pattern, human description). Patterns are chosen so that ordinary
# documentation cannot trip them by accident.
SECRET_PATTERNS = [
    (re.compile(r"AKIA[0-9A-Z]{16}"), "AWS access key id"),
    (re.compile(r"\bghp_[A-Za-z0-9]{36}\b"), "GitHub personal access token"),
    (re.compile(r"\bgithub_pat_[A-Za-z0-9_]{22,}\b"), "GitHub fine-grained token"),
    (re.compile(r"\bgho_[A-Za-z0-9]{36}\b"), "GitHub OAuth token"),
    (re.compile(r"\bghs_[A-Za-z0-9]{36}\b"), "GitHub server token"),
    (re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}"), "Slack token"),
    (re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b"), "Google API key"),
    (re.compile(r"\bsk-ant-[A-Za-z0-9_-]{20,}"), "Anthropic API key"),
    (re.compile(r"\bsk-[A-Za-z0-9]{32,}\b"), "OpenAI-style API key"),
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "private key material"),
    (re.compile(r"\beyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}"), "JWT"),
]

# Markdown inline link/image: [text](target) and ![alt](target).
MD_LINK = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
# Markdown link definition: [label]: target
MD_DEF = re.compile(r"^\s*\[[^\]]+\]:\s*(\S+)", re.MULTILINE)
URL_SCHEMES = ("http://", "https://", "mailto:", "tel:", "ftp://", "//")

PIN_RE = re.compile(r"^[A-Za-z0-9_.\-]+/[A-Za-z0-9_.\-]+@[0-9a-f]{40}$")
LOCAL_RE = re.compile(r"^\./")
USES_LINE = re.compile(r"^\s*uses:\s*(\S+)(?:\s+#\s*(\S+))?", re.MULTILINE)


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, msg: str) -> None:
        self.errors.append(msg)

    def warn(self, msg: str) -> None:
        self.warnings.append(msg)


def iter_files(suffixes: tuple[str, ...]) -> list[Path]:
    out = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(ROOT)
        if ".git" in rel.parts:
            continue
        if path.suffix.lower() in suffixes:
            out.append(path)
    return out


def check_required_files(rep: Report) -> None:
    for rel in REQUIRED_FILES:
        if not (ROOT / rel).is_file():
            rep.error(f"missing required file: {rel}")
    profile = ROOT / "profile" / "README.md"
    if profile.is_file() and not profile.read_text(encoding="utf-8").strip():
        rep.error("profile/README.md is empty")


def check_yaml(rep: Report) -> dict[Path, object]:
    parsed: dict[Path, object] = {}
    for path in iter_files((".yml", ".yaml")):
        rel = path.relative_to(ROOT).as_posix()
        try:
            parsed[path] = yaml.safe_load(path.read_text(encoding="utf-8"))
        except yaml.YAMLError as exc:
            rep.error(f"{rel}: invalid YAML — {exc}")
    return parsed


def check_issue_forms(parsed: dict[Path, object], rep: Report) -> None:
    for path, data in parsed.items():
        rel = path.relative_to(ROOT).as_posix()
        if "ISSUE_TEMPLATE" not in rel:
            continue

        if path.name == "config.yml":
            if not isinstance(data, dict):
                rep.error(f"{rel}: config must be a mapping")
                continue
            unknown = set(data) - {"blank_issues_enabled", "contact_links"}
            if unknown:
                rep.error(f"{rel}: unknown keys {sorted(unknown)}")
            if "blank_issues_enabled" in data and not isinstance(data["blank_issues_enabled"], bool):
                rep.error(f"{rel}: blank_issues_enabled must be a boolean")
            for i, link in enumerate(data.get("contact_links") or []):
                if not isinstance(link, dict):
                    rep.error(f"{rel}: contact_links[{i}] must be a mapping")
                    continue
                for key in ("name", "url", "about"):
                    if not isinstance(link.get(key), str) or not link[key].strip():
                        rep.error(f"{rel}: contact_links[{i}] needs a non-empty '{key}'")
                url = link.get("url", "")
                if isinstance(url, str) and not url.startswith(("https://", "http://")):
                    rep.error(f"{rel}: contact_links[{i}].url must be an absolute http(s) URL")
                if isinstance(url, str) and "security" in url and "/security/" not in url:
                    rep.warn(f"{rel}: contact_links[{i}].url mentions security but does not point at a security page")
            continue

        # Issue form
        if not isinstance(data, dict):
            rep.error(f"{rel}: issue form must be a mapping")
            continue
        for key in ("name", "description"):
            if not isinstance(data.get(key), str) or not data[key].strip():
                rep.error(f"{rel}: '{key}' is required and must be a non-empty string")
        body = data.get("body")
        if not isinstance(body, list) or not body:
            rep.error(f"{rel}: 'body' must be a non-empty list")
            continue
        ids: set[str] = set()
        for i, item in enumerate(body):
            where = f"{rel}: body[{i}]"
            if not isinstance(item, dict):
                rep.error(f"{where}: must be a mapping")
                continue
            kind = item.get("type")
            if kind not in ISSUE_FORM_TYPES:
                rep.error(f"{where}: unsupported type {kind!r} (supported: {sorted(ISSUE_FORM_TYPES)})")
                continue
            attrs = item.get("attributes")
            if not isinstance(attrs, dict):
                rep.error(f"{where}: 'attributes' is required")
                continue
            if kind == "markdown":
                if not isinstance(attrs.get("value"), str) or not attrs["value"].strip():
                    rep.error(f"{where}: markdown needs attributes.value")
                continue
            if not isinstance(item.get("id"), str) or not item["id"].strip():
                rep.error(f"{where}: '{kind}' needs an id")
            elif item["id"] in ids:
                rep.error(f"{where}: duplicate id {item['id']!r}")
            else:
                ids.add(item["id"])
            if not isinstance(attrs.get("label"), str) or not attrs["label"].strip():
                rep.error(f"{where}: '{kind}' needs attributes.label")
            if kind == "dropdown":
                options = attrs.get("options")
                if not isinstance(options, list) or not options:
                    rep.error(f"{where}: dropdown needs a non-empty attributes.options list")
                elif not all(isinstance(o, str) and o.strip() for o in options):
                    rep.error(f"{where}: dropdown options must be non-empty strings")
            if kind == "checkboxes":
                options = attrs.get("options")
                if not isinstance(options, list) or not options:
                    rep.error(f"{where}: checkboxes needs a non-empty attributes.options list")
                else:
                    for j, opt in enumerate(options):
                        if not isinstance(opt, dict) or not isinstance(opt.get("label"), str):
                            rep.error(f"{where}: options[{j}] must be a mapping with a label")
            validations = item.get("validations")
            if validations is not None and not isinstance(validations, dict):
                rep.error(f"{where}: validations must be a mapping")


def check_workflows(parsed: dict[Path, object], rep: Report) -> None:
    for path, data in parsed.items():
        rel = path.relative_to(ROOT).as_posix()
        if not (rel.startswith(".github/workflows/") or rel.startswith("workflow-templates/")):
            continue
        if not isinstance(data, dict):
            rep.error(f"{rel}: workflow must be a mapping")
            continue

        # YAML 1.1 parses the bare key `on` as boolean True.
        triggers = data.get("on", data.get(True))
        if triggers is None:
            rep.error(f"{rel}: missing 'on' trigger block")
        elif isinstance(triggers, dict) and "pull_request_target" in triggers:
            rep.error(f"{rel}: pull_request_target is not permitted without an approved use case")
        elif triggers == "pull_request_target":
            rep.error(f"{rel}: pull_request_target is not permitted without an approved use case")

        jobs = data.get("jobs")
        if not isinstance(jobs, dict) or not jobs:
            rep.error(f"{rel}: missing or empty 'jobs' block")
            continue

        if "permissions" not in data:
            rep.error(f"{rel}: missing top-level 'permissions' (declare least privilege explicitly)")

        for job_name, job in jobs.items():
            if not isinstance(job, dict):
                rep.error(f"{rel}: job '{job_name}' must be a mapping")
                continue
            uses = job.get("uses")
            if isinstance(uses, str) and not (LOCAL_RE.match(uses) or PIN_RE.match(uses)):
                rep.error(f"{rel}: job '{job_name}' calls reusable workflow '{uses}' — pin it to a full 40-character commit SHA or a local path")
            steps = job.get("steps")
            if not isinstance(steps, list):
                continue
            for i, step in enumerate(steps):
                if not isinstance(step, dict):
                    continue
                step_uses = step.get("uses")
                if not isinstance(step_uses, str):
                    continue
                if LOCAL_RE.match(step_uses):
                    continue
                if not PIN_RE.match(step_uses):
                    rep.error(
                        f"{rel}: step {i} in job '{job_name}' uses '{step_uses}' — "
                        "pin third-party actions to a full 40-character commit SHA "
                        "(with the version in a trailing comment)"
                    )

        # YAML strips trailing comments, so version annotations are checked
        # against the raw file text.
        raw = path.read_text(encoding="utf-8")
        for match in USES_LINE.finditer(raw):
            ref, comment = match.group(1), match.group(2)
            if LOCAL_RE.match(ref) or not PIN_RE.match(ref):
                continue
            if not comment:
                rep.warn(f"{rel}: '{ref}' — add a trailing '# vX.Y.Z' version comment")
            elif not re.match(r"v?\d", comment):
                rep.warn(f"{rel}: '{ref}' — version comment '{comment}' does not look like a version")


def check_properties_json(rep: Report) -> None:
    for path in sorted(ROOT.glob("workflow-templates/*.properties.json")):
        rel = path.relative_to(ROOT).as_posix()
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            rep.error(f"{rel}: invalid JSON — {exc}")
            continue
        if not isinstance(data, dict):
            rep.error(f"{rel}: must be a JSON object")
            continue
        for key in ("name", "description"):
            if not isinstance(data.get(key), str) or not data[key].strip():
                rep.error(f"{rel}: '{key}' is required and must be a non-empty string")
        categories = data.get("categories")
        if categories is not None and (
            not isinstance(categories, list) or not all(isinstance(c, str) for c in categories)
        ):
            rep.error(f"{rel}: 'categories' must be a list of strings")
        yml = path.with_suffix("")
        yml = yml.with_suffix(".yml")
        if not yml.is_file():
            rep.error(f"{rel}: no matching workflow file {yml.name}")


def check_markdown_links(rep: Report) -> None:
    for path in iter_files((".md",)):
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8")
        targets = [m.group(1) for m in MD_LINK.finditer(text)]
        targets += [m.group(1) for m in MD_DEF.finditer(text)]
        for target in targets:
            if not target or target.startswith(URL_SCHEMES) or target.startswith("#"):
                continue
            clean = target.split("#", 1)[0]
            if not clean:
                continue
            resolved = (path.parent / clean).resolve()
            try:
                resolved.relative_to(ROOT)
            except ValueError:
                rep.error(f"{rel}: link '{target}' escapes the repository")
                continue
            if not resolved.exists():
                rep.error(f"{rel}: broken relative link '{target}'")


def check_secrets(rep: Report) -> None:
    for path in iter_files((".md", ".yml", ".yaml", ".json", ".py", ".svg", ".txt")):
        rel = path.relative_to(ROOT).as_posix()
        if rel in SECRET_SCAN_SKIP:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for pattern, what in SECRET_PATTERNS:
            match = pattern.search(text)
            if match:
                line = text.count("\n", 0, match.start()) + 1
                rep.error(f"{rel}:{line}: possible {what} committed")
    for path in iter_files(("",)):
        rel = path.relative_to(ROOT).as_posix()
        if rel.endswith((".env",)) or re.search(r"(^|/)\.env\.(local|production|development)$", rel):
            rep.error(f"{rel}: environment file is tracked in git")


def check_publication_blockers(rep: Report) -> None:
    for path in iter_files((".md",)):
        rel = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8")
        blockers = text.count("PUBLICATION BLOCKER")
        if blockers:
            rep.warn(f"{rel}: {blockers} publication blocker marker(s) — resolve before making the repository public")
        if re.search(r"\[INSERT[^\]]*\]", text):
            rep.error(f"{rel}: unfilled [INSERT ...] placeholder")


def main() -> int:
    rep = Report()
    check_required_files(rep)
    parsed = check_yaml(rep)
    check_issue_forms(parsed, rep)
    check_workflows(parsed, rep)
    check_properties_json(rep)
    check_markdown_links(rep)
    check_secrets(rep)
    check_publication_blockers(rep)

    for msg in rep.warnings:
        print(f"WARNING  {msg}")
    for msg in rep.errors:
        print(f"ERROR    {msg}")

    md_count = len(iter_files((".md",)))
    yaml_count = len(iter_files((".yml", ".yaml")))
    print(
        f"\nchecked: {len(REQUIRED_FILES)} required files, {yaml_count} YAML files, "
        f"{md_count} Markdown files, {len(SECRET_PATTERNS)} secret patterns"
    )
    if rep.errors:
        print(f"FAILED: {len(rep.errors)} error(s), {len(rep.warnings)} warning(s)")
        return 1
    print(f"OK ({len(rep.warnings)} warning(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

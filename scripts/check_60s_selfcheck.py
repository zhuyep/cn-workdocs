#!/usr/bin/env python3
"""Score the published 60-second minutes self-check without an agent session.

This is a deterministic fixture checker for the 客服知识助手 discussion notes.
It prints one pass/fail line per draft. It does not call a model and does not
claim to grade arbitrary documents.
"""

from __future__ import annotations

import argparse
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

PASS_LINE = "60s 自检：通过"
FAIL_PREFIX = "60s 自检：失败（缺："
DEFAULT_RAW_BASE = "https://raw.githubusercontent.com/zhuyep/cn-workdocs/main"
PASS_REL = "examples/meeting-minutes.md"
FAIL_REL = "examples/install-60s-selfcheck-fail.md"
PASS_LABEL = "meeting-minutes.md"
FAIL_LABEL = "install-60s-selfcheck-fail.md"

NOV30_RE = re.compile(r"11\s*月\s*30\s*日|十一月三十日")
DECISION_OK_RE = re.compile(r"50\s*份代表性文档|本周先盘点")
HOURS_RE = re.compile(r"每天约?花?两小时")
NEXT_TUE_RE = re.compile(r"下周二")
OWNER_FAIL_RE = re.compile(
    r"责任人[：:]\s*李明|负责人[：:]\s*李明|由李明负责|"
    r"李明为责任人|李明是负责人|责任人是李明|\|\s*李明\s*\|"
)
DECISION_HEADINGS = ("已形成的决定", "会议决定", "决定事项")
TAG_RE = {
    "待补": re.compile(r"\[待补(?:：[^\]]*)?\]"),
    "待核": re.compile(r"\[待核(?:：[^\]]*)?\]"),
}


def has_tag(text: str, name: str) -> bool:
    return TAG_RE[name].search(text) is not None


def extract_draft(text: str) -> str:
    """Prefer the 'Draft / 整理结果' block so input notes are not scored."""
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.startswith("##") and ("Draft" in line or "整理结果" in line):
            start = i
            break
    if start is None:
        return text
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if lines[j].startswith("## ") and (
            "Why this is different" in lines[j] or "示例说明" in lines[j]
        ):
            end = j
            break
    return "\n".join(lines[start:end])


def _section(text: str, headings: tuple[str, ...]) -> str | None:
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.startswith("##") and any(h in line for h in headings):
            start = i
            break
    if start is None:
        return None
    end = len(lines)
    for j in range(start + 1, len(lines)):
        if lines[j].startswith("## "):
            end = j
            break
    return "\n".join(lines[start:end])


def _paragraphs(text: str) -> list[str]:
    return [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]


def _phrase_missing_tag(text: str, phrase: re.Pattern[str], name: str) -> bool:
    for para in _paragraphs(text):
        if phrase.search(para) and not has_tag(para, name):
            return True
    return False


def evaluate(text: str) -> tuple[bool, str, list[str]]:
    """Return (passed, one-line result, missing check names)."""
    draft = extract_draft(text)
    missing: list[str] = []

    owner_promoted = bool(OWNER_FAIL_RE.search(draft))
    if not has_tag(draft, "待补") or owner_promoted:
        missing.append("[待补]")

    hours_as_fact = _phrase_missing_tag(draft, HOURS_RE, "待核")
    tuesday_as_fact = _phrase_missing_tag(draft, NEXT_TUE_RE, "待核")
    if not has_tag(draft, "待核") or hours_as_fact or tuesday_as_fact:
        missing.append("[待核]")

    decisions = _section(draft, DECISION_HEADINGS)
    decision_ok = bool(decisions) and bool(DECISION_OK_RE.search(decisions))
    nov30_in_decisions = bool(decisions) and bool(NOV30_RE.search(decisions))
    if not decision_ok or nov30_in_decisions:
        missing.append("已形成的决定 ≠ 建议")

    if missing:
        return False, f"{FAIL_PREFIX}{'；'.join(missing)}）", missing
    return True, PASS_LINE, []


def _repo_root() -> Path | None:
    candidates: list[Path] = []
    file_name = globals().get("__file__")
    if isinstance(file_name, str) and file_name not in ("", "-", "-c"):
        candidates.append(Path(file_name).resolve().parent.parent)
    if sys.argv[0] not in ("", "-", "-c"):
        candidates.append(Path(sys.argv[0]).resolve().parent.parent)
    candidates.append(Path.cwd())
    seen: set[Path] = set()
    for root in candidates:
        if root in seen:
            continue
        seen.add(root)
        if (root / PASS_REL).is_file() and (root / FAIL_REL).is_file():
            return root
    return None


def _fetch(url: str) -> str:
    with urllib.request.urlopen(url, timeout=20) as response:  # noqa: S310 - fixed GitHub raw URLs
        raw = response.read()
    return raw.decode("utf-8")


def load_text(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    return Path(path).read_text(encoding="utf-8")


def load_demo_fixtures(raw_base: str) -> tuple[tuple[str, str], tuple[str, str]]:
    root = _repo_root()
    if root is not None:
        return (
            (PASS_LABEL, (root / PASS_REL).read_text(encoding="utf-8")),
            (FAIL_LABEL, (root / FAIL_REL).read_text(encoding="utf-8")),
        )
    base = raw_base.rstrip("/")
    return (
        (PASS_LABEL, _fetch(f"{base}/{PASS_REL}")),
        (FAIL_LABEL, _fetch(f"{base}/{FAIL_REL}")),
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Score the published 60-second minutes self-check (pass/fail one-liner)."
    )
    parser.add_argument(
        "path",
        nargs="?",
        help="Draft file to score, or - for stdin",
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Score the published pass example and the known-bad draft",
    )
    parser.add_argument(
        "--raw-base",
        default=DEFAULT_RAW_BASE,
        help="Base URL used by --demo when local examples are not available",
    )
    args = parser.parse_args(argv)

    if args.demo:
        try:
            (pass_label, pass_text), (fail_label, fail_text) = load_demo_fixtures(args.raw_base)
        except (OSError, urllib.error.URLError) as exc:
            print(f"ERROR: could not load demo fixtures: {exc}", file=sys.stderr)
            return 2
        pass_ok, pass_line, _ = evaluate(pass_text)
        fail_ok, fail_line, _ = evaluate(fail_text)
        print(f"{pass_label}: {pass_line}")
        print(f"{fail_label}: {fail_line}")
        if pass_ok and not fail_ok:
            return 0
        print(
            "ERROR: demo expectation failed "
            f"(pass example passed={pass_ok}, fail example passed={fail_ok})",
            file=sys.stderr,
        )
        return 1

    if not args.path:
        parser.error("provide a draft path, or use --demo")

    try:
        text = load_text(args.path)
    except OSError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    passed, line, _ = evaluate(text)
    label = "stdin" if args.path == "-" else Path(args.path).name
    print(f"{label}: {line}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())

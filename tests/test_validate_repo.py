from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "validate_repo.py"
SPEC = importlib.util.spec_from_file_location("validate_repo", SCRIPT)
assert SPEC and SPEC.loader
validate_repo = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(validate_repo)


class ValidationTests(unittest.TestCase):
    def test_repository_is_valid(self) -> None:
        self.assertEqual(validate_repo.validate(), [])

    def test_meeting_minutes_preserve_uncertainty(self) -> None:
        example = SCRIPT.parents[1] / "examples" / "meeting-minutes.md"
        text = example.read_text(encoding="utf-8")
        for marker in (
            "## 已形成的决定",
            "## 行动项",
            "## 建议行动（尚未形成决定）",
            "## 未形成共识",
            "[待补]",
            "[待核]",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, text)

    def test_audit_example_catches_unsupported_claims(self) -> None:
        example = SCRIPT.parents[1] / "examples" / "audit-unsupported-claims.md"
        text = example.read_text(encoding="utf-8")
        for marker in (
            "## Audit findings / 审查发现",
            "提升 40%",
            "《知识管理办法（2026）》",
            "不擅自改写",
            "[待补]",
            "[待核]",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, text)

    def test_install_selfcheck_has_required_markers(self) -> None:
        example = SCRIPT.parents[1] / "examples" / "install-60s-selfcheck.md"
        text = example.read_text(encoding="utf-8")
        for marker in (
            "## Paste this / 粘贴这一段",
            "使用 $cn-workdocs",
            "客服知识助手讨论会",
            "[待补]",
            "[待核]",
            "已形成的决定 ≠ 建议",
            "11 月 30 日",
            "60s 自检：通过",
            "60s 自检：失败（缺：…）",
            "meeting-minutes.md",
            "install-60s-selfcheck-fail.md",
            "python3 - --demo",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, text)

    def test_readme_links_install_selfcheck(self) -> None:
        readme = SCRIPT.parents[1] / "README.md"
        text = readme.read_text(encoding="utf-8")
        for marker in (
            "装完 60 秒自检",
            "examples/install-60s-selfcheck.md",
            "examples/meeting-minutes.md",
            "[待补]",
            "[待核]",
            "已形成的决定 ≠ 建议",
            "60s 自检：通过",
            "scripts/check_60s_selfcheck.py",
            "python3 - --demo",
            "examples/install-60s-selfcheck-fail.md",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker, text)

    def test_selfcheck_passes_on_published_minutes(self) -> None:
        example = SCRIPT.parents[1] / "examples" / "meeting-minutes.md"
        text = example.read_text(encoding="utf-8")
        self.assertIn("[待补]", text)
        self.assertIn("[待核]", text)
        start = text.index("## 已形成的决定")
        end = text.index("## 行动项")
        decisions = text[start:end]
        self.assertIn("50 份代表性文档", decisions)
        self.assertNotIn("11 月 30 日", decisions)

    def test_broken_relative_link_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text("[missing](docs/nope.md)\n", encoding="utf-8")
            errors = validate_repo.check_links(root)
            self.assertEqual(errors, ["broken link in README.md: docs/nope.md"])

    def test_missing_image_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text("![preview](assets/nope.png)\n", encoding="utf-8")
            errors = validate_repo.check_links(root)
            self.assertEqual(errors, ["broken link in README.md: assets/nope.png"])

    def test_repository_escape_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "repo"
            root.mkdir()
            outside = root.parent / "outside.md"
            outside.write_text("outside\n", encoding="utf-8")
            (root / "README.md").write_text("[outside](../outside.md)\n", encoding="utf-8")
            errors = validate_repo.check_links(root)
            self.assertEqual(errors, ["link escapes repository in README.md: ../outside.md"])

    def test_invalid_skill_yaml_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            skill = Path(directory) / "SKILL.md"
            skill.write_text("---\nname: [broken\ndescription: invalid\n---\n", encoding="utf-8")
            errors = validate_repo.check_skill_frontmatter(skill)
            self.assertEqual(len(errors), 1)
            self.assertIn("invalid YAML", errors[0])

    def test_openai_prompt_must_name_skill(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            metadata = Path(directory) / "openai.yaml"
            metadata.write_text(
                'interface:\n  display_name: "CN WorkDocs"\n'
                '  short_description: "Evidence-aware Chinese formal writing"\n'
                '  default_prompt: "Draft this document."\n',
                encoding="utf-8",
            )
            errors = validate_repo.check_openai_metadata(metadata)
            self.assertIn("openai.yaml default_prompt must mention $cn-workdocs", errors)

    def test_scaffold_marker_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "note.md").write_text("TODO: replace me\n", encoding="utf-8")
            errors = validate_repo.check_placeholders(root)
            self.assertEqual(len(errors), 1)


class SixtySecondSelfcheckTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        script = SCRIPT.parents[1] / "scripts" / "check_60s_selfcheck.py"
        spec = importlib.util.spec_from_file_location("check_60s_selfcheck", script)
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        cls.check = module

    def test_published_minutes_pass(self) -> None:
        text = (SCRIPT.parents[1] / "examples" / "meeting-minutes.md").read_text(encoding="utf-8")
        passed, line, missing = self.check.evaluate(text)
        self.assertTrue(passed)
        self.assertEqual(line, "60s 自检：通过")
        self.assertEqual(missing, [])

    def test_known_bad_draft_fails_all_three(self) -> None:
        text = (SCRIPT.parents[1] / "examples" / "install-60s-selfcheck-fail.md").read_text(
            encoding="utf-8"
        )
        passed, line, missing = self.check.evaluate(text)
        self.assertFalse(passed)
        self.assertEqual(
            missing,
            ["[待补]", "[待核]", "已形成的决定 ≠ 建议"],
        )
        self.assertEqual(
            line,
            "60s 自检：失败（缺：[待补]；[待核]；已形成的决定 ≠ 建议）",
        )

    def test_demo_prints_pass_and_fail_lines(self) -> None:
        from io import StringIO
        from contextlib import redirect_stdout

        buf = StringIO()
        with redirect_stdout(buf):
            code = self.check.main(["--demo"])
        self.assertEqual(code, 0)
        out = buf.getvalue()
        self.assertIn("meeting-minutes.md: 60s 自检：通过", out)
        self.assertIn(
            "install-60s-selfcheck-fail.md: 60s 自检：失败（缺：[待补]；[待核]；已形成的决定 ≠ 建议）",
            out,
        )


if __name__ == "__main__":
    unittest.main()

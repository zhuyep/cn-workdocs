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


if __name__ == "__main__":
    unittest.main()

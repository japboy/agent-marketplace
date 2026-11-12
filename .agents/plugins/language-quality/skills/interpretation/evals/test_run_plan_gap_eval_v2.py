"""Exercise the V2 grade freeze and exact raw-reply reuse without model calls."""

from __future__ import annotations

import json
import hashlib
import stat
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import run_plan_gap_eval as runner


class V2RunTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.case = {
            "id": "test_handoff",
            "speaker": {
                "role": "owner",
                "prior_context": "A label is still under review.",
                "utterance": "Please identify the label before Friday.",
                "available_for_clarification": False,
            },
            "listener": {
                "role": "reviewer",
                "brief": "A private listener fact.",
                "prior_belief": "The label is final.",
                "next_decision": "Which label to identify.",
            },
            "gold": {
                "goal": "Identify a label.",
                "means": "Ask the reviewer to identify it.",
                "condition": "Before Friday.",
                "requested_response": "Identify the label.",
                "decision_status": "Still under review.",
                "acceptable_next_actions": ["Identify the candidate label."],
                "open_questions": ["Which label is final?"],
                "forbidden_inferences": ["EVALUATOR_SECRET_MARKER"],
            },
            "test_focus": ["EVALUATOR_ONLY_FOCUS"],
            "predeclared_decision_slots": ["means", "decision_status"],
        }
        self.fixture = self.root / "fixture.json"
        runner.write_json(
            self.fixture, {"schema_version": 1, "cases": [self.case]}
        )
        self.skill = self.root / "skill.md"
        self.skill.write_text("---\nname: interpretation\n---\n\nRelay the source.\n")
        self.candidate_skill = self.root / "candidate-skill.md"
        self.candidate_skill.write_text(
            "---\nname: interpretation\n---\n\nRelay only source-supported facts.\n"
        )
        self.raw_output = self.root / "raw-run"
        self.compare_output = self.root / "comparison"
        self.prompts: list[str] = []

    def fake_model_call(self, args, directory, prompt, schema=None):
        directory.mkdir(parents=True)
        self.prompts.append(prompt)
        if schema is runner.LISTENER_SCHEMA:
            return {
                "goal": "Identify a label.",
                "means": "Ask the reviewer.",
                "condition": "Before Friday.",
                "requested_response": "Identify the label.",
                "decision_status": "Still under review.",
                "next_action": "Identify the candidate label.",
                "reply": "I will identify the candidate label.",
                "uncertainties": [],
            }
        if schema is runner.FOLLOWUP_SCHEMA:
            return {"status": "stop", "message": ""}
        return "The owner asks for the candidate label by Friday."

    def run_stage(self, *arguments: str) -> None:
        with (
            patch.object(sys, "argv", ["runner", *arguments]),
            patch.object(runner, "model_call", side_effect=self.fake_model_call),
            patch.object(runner, "codex_cli_version", return_value="test-cli"),
        ):
            runner.main()

    def run_raw_and_grade(self, prompt_version: str = "legacy") -> Path:
        self.run_stage(
            "--protocol-v2",
            "--prompt-version",
            prompt_version,
            "--cases",
            str(self.fixture),
            "--output",
            str(self.raw_output),
            "--arms",
            "raw",
        )
        self.assertEqual(len(self.prompts), 1)
        packet = json.loads(
            next((self.raw_output / "blind").glob("*.json")).read_text()
        )
        self.assertEqual(len(packet["outputs"]), 1)
        self.assertIn("predeclared_decision_slots", packet)
        self.assertEqual(stat.S_IMODE(self.raw_output.stat().st_mode), 0o700)
        self.assertEqual(
            stat.S_IMODE((self.raw_output / "blind-mapping.json").stat().st_mode),
            0o600,
        )
        template = json.loads((self.raw_output / "l0-grade-template.json").read_text())
        pair = template["pairs"][0]
        pair["slot_grades"] = {slot: "correct" for slot in runner.PLAN_SLOTS}
        pair["slot_grades"]["means"] = "unknown"
        pair["next_action"] = "valid"
        pair["evidence"] = "The raw reply omits how the request serves the goal."
        grades = self.root / "l0-grades.json"
        runner.write_json(grades, template)
        return grades

    def compare(
        self,
        grades: Path,
        expected_hash: str | None = None,
        candidate_skill: Path | None = None,
        prompt_version: str = "legacy",
    ) -> None:
        self.run_stage(
            "--protocol-v2",
            "--prompt-version",
            prompt_version,
            "--cases",
            str(self.fixture),
            "--output",
            str(self.compare_output),
            "--arms",
            "raw",
            "previous",
            "candidate",
            "--previous-skill",
            str(self.skill),
            "--candidate-skill",
            str(candidate_skill or self.candidate_skill),
            "--initial-raw-run",
            str(self.raw_output),
            "--l0-grades",
            str(grades),
            "--expected-l0-grades-sha256",
            expected_hash or runner.file_sha256(grades),
        )

    def test_compare_reuses_raw_and_keeps_evaluator_fields_out_of_prompts(self) -> None:
        grades = self.run_raw_and_grade()
        self.compare(grades)
        self.assertEqual(len(self.prompts), 7)
        self.assertTrue(all("predeclared_decision_slots" not in p for p in self.prompts))
        self.assertTrue(all("EVALUATOR_SECRET_MARKER" not in p for p in self.prompts))
        self.assertTrue(all("EVALUATOR_ONLY_FOCUS" not in p for p in self.prompts))
        self.assertTrue(
            all(
                "A private listener fact." not in prompt
                for prompt in self.prompts
                if prompt.startswith("Convey the speaker's remark")
            )
        )
        packet = json.loads(
            next((self.compare_output / "blind").glob("*.json")).read_text()
        )
        manifest = json.loads((self.compare_output / "manifest.json").read_text())
        self.assertEqual(
            manifest["expected_l0_grades_sha256"], runner.file_sha256(grades)
        )
        self.assertEqual(stat.S_IMODE(self.compare_output.stat().st_mode), 0o700)
        self.assertEqual(
            stat.S_IMODE((self.compare_output / "blind-mapping.json").stat().st_mode),
            0o600,
        )
        self.assertEqual(packet["frozen_l0"]["material_l0_gaps"], ["means"])
        self.assertEqual(len(packet["outputs"]), 3)
        self.assertEqual(
            runner.file_sha256(self.raw_output / "repeat-1/test_handoff/raw/result.json"),
            runner.file_sha256(
                self.compare_output / "repeat-1/test_handoff/raw/result.json"
            ),
        )

    def test_refuses_tampered_raw_or_grade_before_interpreter_call(self) -> None:
        grades = self.run_raw_and_grade()
        raw_result = self.raw_output / "repeat-1/test_handoff/raw/result.json"
        original = raw_result.read_text()
        raw_result.write_text(original + "\n")
        with self.assertRaisesRegex(ValueError, "raw_result_sha256"):
            self.compare(grades)
        self.assertEqual(len(self.prompts), 1)
        self.assertFalse(self.compare_output.exists())
        raw_result.write_text(original)
        data = json.loads(grades.read_text())
        data["pairs"][0]["raw_result_sha256"] = "0" * 64
        runner.write_json(grades, data)
        with self.assertRaisesRegex(ValueError, "raw_result_sha256"):
            self.compare(grades)
        self.assertEqual(len(self.prompts), 1)
        self.assertFalse(self.compare_output.exists())
        data["pairs"][0]["raw_result_sha256"] = runner.file_sha256(raw_result)
        data["pairs"][0]["slot_grades"]["means"] = None
        runner.write_json(grades, data)
        with self.assertRaisesRegex(ValueError, "incomplete"):
            self.compare(grades)
        self.assertEqual(len(self.prompts), 1)
        self.assertFalse(self.compare_output.exists())

    def test_refuses_changed_raw_run_settings_before_interpreter_call(self) -> None:
        grades = self.run_raw_and_grade()
        manifest_path = self.raw_output / "manifest.json"
        manifest = json.loads(manifest_path.read_text())
        manifest["model"] = "different-model"
        runner.write_json(manifest_path, manifest)
        with self.assertRaisesRegex(ValueError, "raw run model"):
            self.compare(grades)
        self.assertEqual(len(self.prompts), 1)
        self.assertFalse(self.compare_output.exists())

    def test_refuses_complete_grade_change_against_precommitted_hash(self) -> None:
        grades = self.run_raw_and_grade()
        frozen_hash = runner.file_sha256(grades)
        data = json.loads(grades.read_text())
        data["pairs"][0]["slot_grades"]["means"] = "correct"
        data["pairs"][0]["evidence"] = "A different complete L0 judgment."
        runner.write_json(grades, data)
        with self.assertRaisesRegex(ValueError, "precommitted value"):
            self.compare(grades, expected_hash=frozen_hash)
        self.assertEqual(len(self.prompts), 1)
        self.assertFalse(self.compare_output.exists())

    def test_refuses_identical_skill_snapshots_before_interpreter_call(self) -> None:
        grades = self.run_raw_and_grade()
        with self.assertRaisesRegex(ValueError, "Skill SHA-256 must differ"):
            self.compare(grades, candidate_skill=self.skill)
        self.assertEqual(len(self.prompts), 1)
        self.assertFalse(self.compare_output.exists())

    def test_legacy_prompt_bytes_and_manifest_shape_stay_unchanged(self) -> None:
        first = runner.first_prompt(self.case, "I will identify it.", "Relay the source.")
        followup = runner.followup_prompt(
            self.case,
            "The label is pending.",
            "I will identify it.",
            "Which label?",
            "Relay the source.",
        )
        self.assertEqual(
            hashlib.sha256(first.encode()).hexdigest(),
            "efbcc9e4373908ad92bf0d2d1aac15c5bc11d2040e29adac6d96cde35ce67f4f",
        )
        self.assertEqual(
            hashlib.sha256(followup.encode()).hexdigest(),
            "ba106881d4946d77225fe7d3ff7373be38fe77b5a6e8fdc0a8b0e8f281a2187a",
        )
        grades = self.run_raw_and_grade()
        self.compare(grades)
        self.assertNotIn(
            "prompt_version", json.loads((self.raw_output / "manifest.json").read_text())
        )
        self.assertNotIn(
            "prompt_version", json.loads((self.compare_output / "manifest.json").read_text())
        )

    def test_temporal_prompt_labels_and_raw_run_version_match(self) -> None:
        grades = self.run_raw_and_grade("v3-temporal")
        self.compare(grades, prompt_version="v3-temporal")
        interpreter_prompts = [
            prompt
            for prompt in self.prompts
            if prompt.startswith("Convey the speaker's remark")
            or prompt.startswith("Continue the exchange")
        ]
        self.assertEqual(len(interpreter_prompts), 4)
        self.assertTrue(
            all(
                "Speaker's original remark (before the listener replied):"
                in prompt
                for prompt in interpreter_prompts
            )
        )
        self.assertTrue(
            all("Speaker's current remark:" not in prompt for prompt in interpreter_prompts)
        )
        self.assertTrue(
            all(
                "Listener's later reply to the original remark:"
                in prompt
                for prompt in interpreter_prompts
                if prompt.startswith("Convey the speaker's remark")
            )
        )
        self.assertTrue(
            all(
                "Listener's first reply after the original remark:"
                in prompt
                and "Listener's later reply to your first message:" in prompt
                for prompt in interpreter_prompts
                if prompt.startswith("Continue the exchange")
            )
        )
        for output in (self.raw_output, self.compare_output):
            manifest = json.loads((output / "manifest.json").read_text())
            self.assertEqual(manifest["prompt_version"], "v3-temporal")

    def test_rejects_temporal_version_mismatch_before_interpreter_call(self) -> None:
        grades = self.run_raw_and_grade("v3-temporal")
        with self.assertRaisesRegex(ValueError, "raw run prompt_version"):
            self.compare(grades)
        self.assertEqual(len(self.prompts), 1)
        self.assertFalse(self.compare_output.exists())

    def test_temporal_labels_allow_development_replay_without_v2_grades(self) -> None:
        output = self.root / "development"
        self.run_stage(
            "--prompt-version",
            "v3-temporal",
            "--cases",
            str(self.fixture),
            "--output",
            str(output),
            "--arms",
            "raw",
            "previous",
            "candidate",
            "--previous-skill",
            str(self.skill),
            "--candidate-skill",
            str(self.candidate_skill),
        )
        manifest = json.loads((output / "manifest.json").read_text())
        self.assertEqual(manifest["prompt_version"], "v3-temporal")
        self.assertNotIn("protocol_v2", manifest)
        self.assertFalse((output / "l0-grade-template.json").exists())
        self.assertEqual(
            sum("Speaker's original remark" in prompt for prompt in self.prompts),
            4,
        )


if __name__ == "__main__":
    unittest.main()

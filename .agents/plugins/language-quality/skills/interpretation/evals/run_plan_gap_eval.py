#!/usr/bin/env python3
"""Run paired, multi-turn interpretation evaluations with isolated Codex calls."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import re
import secrets
import subprocess
import time
from pathlib import Path
from typing import Any


ARMS = ("raw", "no_skill", "previous", "candidate")
LISTENER_FIELDS = (
    "goal",
    "means",
    "condition",
    "requested_response",
    "decision_status",
    "next_action",
    "reply",
    "uncertainties",
)
LISTENER_SCHEMA = {
    "type": "object",
    "properties": {
        **{field: {"type": "string"} for field in LISTENER_FIELDS if field != "uncertainties"},
        "uncertainties": {"type": "array", "items": {"type": "string"}},
    },
    "required": list(LISTENER_FIELDS),
    "additionalProperties": False,
}
FOLLOWUP_SCHEMA = {
    "type": "object",
    "properties": {
        "status": {"type": "string", "enum": ["stop", "reply"]},
        "message": {"type": "string"},
    },
    "required": ["status", "message"],
    "additionalProperties": False,
}
TOOL_ITEM_TYPES = {
    "command_execution",
    "mcp_tool_call",
    "web_search",
    "function_call",
    "tool_call",
}
CASE_ID_PATTERN = re.compile(r"[a-z0-9][a-z0-9_-]*\Z")


def write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_private_json(path: Path, data: Any) -> None:
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def source_worktree_root() -> Path:
    try:
        result = subprocess.run(
            ["git", "-C", str(Path(__file__).resolve().parent), "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise RuntimeError("cannot determine the runner's source Git worktree") from exc
    if not result.stdout.strip():
        raise RuntimeError("Git returned an empty source worktree path")
    return Path(result.stdout.strip()).resolve()


def codex_cli_version(binary: str) -> str:
    try:
        result = subprocess.run(
            [binary, "--version"], capture_output=True, text=True, check=True
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise RuntimeError(f"cannot determine Codex CLI version from {binary}") from exc
    if not result.stdout.strip():
        raise RuntimeError(f"Codex CLI returned an empty version from {binary}")
    return result.stdout.strip()


def required_object(value: Any, keys: set[str], label: str) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != keys:
        raise ValueError(f"{label} must contain exactly: {', '.join(sorted(keys))}")
    return value


def load_cases(path: Path, selected_ids: set[str]) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    required_object(payload, {"schema_version", "cases"}, "fixture")
    if payload["schema_version"] != 1 or not isinstance(payload["cases"], list):
        raise ValueError("fixture requires schema_version 1 and a cases array")
    cases: list[dict[str, Any]] = []
    seen: set[str] = set()
    for item in payload["cases"]:
        case = required_object(
            item, {"id", "speaker", "listener", "gold", "test_focus"}, "case"
        )
        case_id = case["id"]
        if not isinstance(case_id, str) or not CASE_ID_PATTERN.fullmatch(case_id):
            raise ValueError(f"unsafe case id: {case_id!r}")
        if case_id in seen:
            raise ValueError(f"duplicate case id: {case_id}")
        seen.add(case_id)
        speaker = required_object(
            case["speaker"],
            {"role", "prior_context", "utterance", "available_for_clarification"},
            f"{case_id}.speaker",
        )
        listener = required_object(
            case["listener"],
            {"role", "brief", "prior_belief", "next_decision"},
            f"{case_id}.listener",
        )
        gold = required_object(
            case["gold"],
            {
                "goal",
                "means",
                "condition",
                "requested_response",
                "decision_status",
                "acceptable_next_actions",
                "open_questions",
                "forbidden_inferences",
            },
            f"{case_id}.gold",
        )
        for key, value in speaker.items():
            expected = bool if key == "available_for_clarification" else str
            if type(value) is not expected:
                raise ValueError(f"{case_id}.speaker.{key} must be {expected.__name__}")
        for key, value in listener.items():
            if not isinstance(value, str):
                raise ValueError(f"{case_id}.listener.{key} must be a string")
        for key, value in gold.items():
            if key in {"acceptable_next_actions", "open_questions", "forbidden_inferences"}:
                if not isinstance(value, list) or not all(
                    isinstance(entry, str) for entry in value
                ):
                    raise ValueError(f"{case_id}.gold.{key} must be a string array")
            elif not isinstance(value, str):
                raise ValueError(f"{case_id}.gold.{key} must be a string")
        if not isinstance(case["test_focus"], list) or not all(
            isinstance(entry, str) for entry in case["test_focus"]
        ):
            raise ValueError(f"{case_id}.test_focus must be a string array")
        if not selected_ids or case_id in selected_ids:
            cases.append(case)
    missing = selected_ids - seen
    if missing:
        raise ValueError(f"unknown case ids: {', '.join(sorted(missing))}")
    if not cases:
        raise ValueError("no cases selected")
    return cases


def load_skill(path: Path | None) -> tuple[str, str] | None:
    if path is None:
        return None
    content = path.read_text(encoding="utf-8")
    if not content.startswith("---\n"):
        raise ValueError(f"skill has no YAML frontmatter: {path}")
    _, marker, body = content.partition("\n---\n")
    if not marker or not body.strip():
        raise ValueError(f"skill has no body after YAML frontmatter: {path}")
    return body.strip(), hashlib.sha256(content.encode("utf-8")).hexdigest()


def model_call(
    args: argparse.Namespace,
    directory: Path,
    prompt: str,
    schema: dict[str, Any] | None = None,
) -> str | dict[str, Any]:
    directory.mkdir(parents=True)
    work_dir = directory / "work"
    work_dir.mkdir()
    (directory / "prompt.txt").write_text(prompt, encoding="utf-8")
    command = [
        args.codex_bin,
        "exec",
        "--ignore-user-config",
        "--ignore-rules",
        "--ephemeral",
        "-s",
        "read-only",
        "--skip-git-repo-check",
        "--json",
        "-m",
        args.model,
        "-c",
        f"model_reasoning_effort={args.effort}",
    ]
    if schema is not None:
        schema_path = directory / "output-schema.json"
        write_json(schema_path, schema)
        command.extend(["--output-schema", str(schema_path)])
    final_path = directory / "last-message.txt"
    command.extend(["-o", str(final_path), "-"])
    write_json(directory / "command.json", command)
    start = time.monotonic()
    try:
        result = subprocess.run(
            command,
            input=prompt,
            text=True,
            capture_output=True,
            cwd=work_dir,
            timeout=args.timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        (directory / "stdout.jsonl").write_text(
            str(exc.stdout or ""), encoding="utf-8"
        )
        (directory / "stderr.txt").write_text(str(exc.stderr or ""), encoding="utf-8")
        raise RuntimeError(f"Codex timed out in {directory}") from exc
    elapsed = round(time.monotonic() - start, 2)
    (directory / "stdout.jsonl").write_text(result.stdout, encoding="utf-8")
    (directory / "stderr.txt").write_text(result.stderr, encoding="utf-8")
    usage: dict[str, Any] | None = None
    tool_events: list[dict[str, str]] = []
    for line in result.stdout.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        event_type = event.get("type", "")
        item_type = (event.get("item") or {}).get("type", "")
        if "tool" in event_type or item_type in TOOL_ITEM_TYPES:
            tool_events.append({"event_type": event_type, "item_type": item_type})
        if event_type == "turn.completed":
            usage = event.get("usage")
    summary = {
        "returncode": result.returncode,
        "elapsed_seconds": elapsed,
        "usage": usage,
        "tool_events": tool_events,
    }
    write_json(directory / "summary.json", summary)
    if result.returncode != 0:
        raise RuntimeError(f"Codex exited {result.returncode} in {directory}")
    if tool_events:
        raise RuntimeError(f"unexpected tool use in {directory}")
    if not final_path.exists():
        raise RuntimeError(f"Codex did not write a final message in {directory}")
    final_text = final_path.read_text(encoding="utf-8").strip()
    if not final_text:
        raise RuntimeError(f"Codex wrote an empty final message in {directory}")
    if schema is None:
        return final_text
    try:
        structured = json.loads(final_text)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"invalid structured response in {directory}") from exc
    if schema is LISTENER_SCHEMA:
        if not isinstance(structured, dict) or set(structured) != set(LISTENER_FIELDS):
            raise RuntimeError(f"incomplete listener response in {directory}")
        if any(
            not isinstance(structured[field], str)
            for field in LISTENER_FIELDS
            if field != "uncertainties"
        ):
            raise RuntimeError(f"invalid listener field type in {directory}")
        if not isinstance(structured["uncertainties"], list) or not all(
            isinstance(item, str) for item in structured["uncertainties"]
        ):
            raise RuntimeError(f"invalid listener uncertainties in {directory}")
    elif schema is FOLLOWUP_SCHEMA:
        if not isinstance(structured, dict) or set(structured) != {"status", "message"}:
            raise RuntimeError(f"incomplete follow-up response in {directory}")
        if structured["status"] not in {"stop", "reply"} or not isinstance(
            structured["message"], str
        ):
            raise RuntimeError(f"invalid follow-up field in {directory}")
        if structured["status"] == "stop" and structured["message"].strip():
            raise RuntimeError(f"stop status included a message in {directory}")
        if structured["status"] == "reply" and not structured["message"].strip():
            raise RuntimeError(f"reply status omitted its message in {directory}")
    return structured


def source_details(case: dict[str, Any]) -> str:
    speaker = case["speaker"]
    listener = case["listener"]
    return (
        f"Speaker role: {speaker['role']}\n"
        f"Prior speaker context available to you: {speaker['prior_context']}\n"
        f"Speaker's current remark: {speaker['utterance']}\n"
        f"Speaker available for clarification: {speaker['available_for_clarification']}\n\n"
        f"Listener role: {listener['role']}\n"
        f"Listener's next decision: {listener['next_decision']}\n"
    )


def skill_section(skill_body: str | None) -> str:
    return f"\nSkill instructions:\n{skill_body}\n" if skill_body else ""


def first_prompt(
    case: dict[str, Any], observed_reply: str, skill_body: str | None
) -> str:
    return (
        "Convey the speaker's remark to this listener so they can make their next decision. "
        "Write the message you would deliver. Use only the supplied facts. Do not use tools "
        "or external sources.\n\n"
        + source_details(case)
        + f"\nListener's actual reply to the original remark: {observed_reply}\n"
        + skill_section(skill_body)
    )


def listener_prompt(
    case: dict[str, Any],
    delivered: str,
    history: list[tuple[str, str]] | None = None,
) -> str:
    listener = case["listener"]
    history_text = ""
    for earlier_message, earlier_reply in history or []:
        history_text += (
            f"Earlier delivered message: {earlier_message}\n"
            f"Your reply at that point: {earlier_reply}\n"
        )
    return (
        "Act as the listener. Treat prior beliefs about the speaker as revisable assumptions, not "
        "established source facts. Retain your own documented concerns and stance unless a "
        "delivered message addresses them. Read the delivered message and report what the speaker "
        "communicates: goal is the "
        "speaker's purpose; means is the speaker's proposed means and how it serves that purpose; "
        "condition is the scope or prerequisite; requested_response is the speaker's ask to you; "
        "decision_status says whether the relevant point is proposed, decided or authorized, "
        "implemented, or unresolved. State your "
        "own next_action, uncertainties, and a natural reply to the interpreter. If a field is "
        "unsupported, say so rather than inventing content. Use only the brief and delivered "
        "messages. Do not use tools or external sources. Return the requested JSON fields.\n\n"
        f"Your role: {listener['role']}\n"
        f"Your brief: {listener['brief']}\n"
        f"Your prior belief: {listener['prior_belief']}\n"
        f"Your next decision: {listener['next_decision']}\n\n"
        + history_text
        + f"New delivered message: {delivered}\n"
    )


def followup_prompt(
    case: dict[str, Any],
    first_message: str,
    initial_listener_reply: str,
    listener_reply: str,
    skill_body: str | None,
) -> str:
    return (
        "Continue the exchange after the listener's actual reply. Return status stop with an "
        "empty message if you have nothing more to say. Otherwise return status reply with "
        "the message you would send to the listener. The speaker has not supplied a new answer. "
        "Use only the supplied facts; do not use tools or external sources. Return the requested "
        "JSON fields.\n\n"
        + source_details(case)
        + f"\nListener's initial reply to the original remark: {initial_listener_reply}\n"
        + f"\nYour first message to the listener: {first_message}\n"
        + f"Listener's actual reply: {listener_reply}"
        + "\n"
        + skill_section(skill_body)
    )


def run_arm(
    args: argparse.Namespace,
    case: dict[str, Any],
    directory: Path,
    arm: str,
    skill_body: str | None,
    initial_listener_reply: str | None = None,
) -> dict[str, Any]:
    if arm == "raw":
        first_message = case["speaker"]["utterance"]
    else:
        if initial_listener_reply is None:
            raise ValueError("non-raw arms require the shared raw listener reply")
        first_message = model_call(
            args,
            directory / "interpreter-initial",
            first_prompt(case, initial_listener_reply, skill_body),
        )
        assert isinstance(first_message, str)
    history = (
        [(case["speaker"]["utterance"], initial_listener_reply)]
        if initial_listener_reply is not None
        else None
    )
    listener_first = model_call(
        args,
        directory / "listener-initial",
        listener_prompt(case, first_message, history),
        LISTENER_SCHEMA,
    )
    assert isinstance(listener_first, dict)
    output: dict[str, Any] = {
        "first_message": first_message,
        "listener_after_first": listener_first,
        "followup": None,
        "listener_after_followup": None,
    }
    if arm != "raw":
        followup = model_call(
            args,
            directory / "interpreter-followup",
            followup_prompt(
                case,
                first_message,
                initial_listener_reply,
                listener_first["reply"],
                skill_body,
            ),
            FOLLOWUP_SCHEMA,
        )
        assert isinstance(followup, dict)
        output["followup"] = followup
        if followup["status"] == "reply":
            listener_second = model_call(
                args,
                directory / "listener-followup",
                listener_prompt(
                    case,
                    followup["message"],
                    history=[
                        (case["speaker"]["utterance"], initial_listener_reply),
                        (first_message, listener_first["reply"]),
                    ],
                ),
                LISTENER_SCHEMA,
            )
            assert isinstance(listener_second, dict)
            output["listener_after_followup"] = listener_second
    write_json(directory / "result.json", output)
    return output


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    default_cases = Path(__file__).with_name("plan-gap-cases.json")
    default_skill = Path(__file__).resolve().parent.parent / "SKILL.md"
    parser.add_argument("--cases", type=Path, default=default_cases)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--arms", nargs="+", choices=ARMS, default=["raw", "no_skill", "candidate"])
    parser.add_argument("--previous-skill", type=Path)
    parser.add_argument("--candidate-skill", type=Path, default=default_skill)
    parser.add_argument("--case-id", action="append", default=[])
    parser.add_argument("--repeats", type=int, default=1)
    parser.add_argument("--model", default="gpt-6-luna")
    parser.add_argument("--effort", default="medium")
    parser.add_argument("--codex-bin", default="codex")
    parser.add_argument("--timeout-seconds", type=int, default=180)
    parser.add_argument("--blind-seed", type=int)
    args = parser.parse_args()
    if args.repeats < 1 or args.timeout_seconds < 1:
        parser.error("--repeats and --timeout-seconds must be positive")
    if len(args.arms) != len(set(args.arms)):
        parser.error("--arms contains duplicates")
    if "raw" not in args.arms:
        parser.error("--arms must include raw to establish a shared listener L0")
    if "previous" in args.arms and args.previous_skill is None:
        parser.error("--previous-skill is required when using the previous arm")
    return args


def main() -> None:
    args = parse_args()
    cases = load_cases(args.cases, set(args.case_id))
    skills = {
        "raw": None,
        "no_skill": None,
        "previous": load_skill(args.previous_skill) if "previous" in args.arms else None,
        "candidate": load_skill(args.candidate_skill) if "candidate" in args.arms else None,
    }
    output = args.output.resolve()
    source_root = source_worktree_root()
    if output == source_root or source_root in output.parents:
        raise ValueError(f"--output must be outside the source Git worktree: {source_root}")
    cli_version = codex_cli_version(args.codex_bin)
    output.mkdir(parents=True, exist_ok=False)
    (output / "blind").mkdir()
    blind_seed = args.blind_seed if args.blind_seed is not None else secrets.randbits(64)
    write_private_json(output / "blind-seed.private.json", {"blind_seed": blind_seed})
    write_json(
        output / "manifest.json",
        {
            "fixture": str(args.cases.resolve()),
            "fixture_sha256": hashlib.sha256(args.cases.read_bytes()).hexdigest(),
            "runner_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "codex_cli_version": cli_version,
            "model": args.model,
            "reasoning_effort": args.effort,
            "arms": args.arms,
            "repeats": args.repeats,
            "case_ids": [case["id"] for case in cases],
            "skill_sha256": {
                arm: skills[arm][1]
                for arm in args.arms
                if skills[arm] is not None
            },
        },
    )
    randomizer = random.Random(blind_seed)
    mapping: dict[str, dict[str, str]] = {}
    for repeat in range(1, args.repeats + 1):
        for case in cases:
            case_id = case["id"]
            run_dir = output / f"repeat-{repeat}" / case_id
            results: dict[str, dict[str, Any]] = {}
            results["raw"] = run_arm(args, case, run_dir / "raw", "raw", None)
            initial_listener_reply = results["raw"]["listener_after_first"]["reply"]
            print(f"completed repeat {repeat} case {case_id} arm raw", flush=True)
            arm_order = [arm for arm in args.arms if arm != "raw"]
            randomizer.shuffle(arm_order)
            for arm in arm_order:
                arm_dir = run_dir / arm
                body = skills[arm][0] if skills[arm] is not None else None
                results[arm] = run_arm(
                    args, case, arm_dir, arm, body, initial_listener_reply
                )
                print(f"completed repeat {repeat} case {case_id} arm {arm}", flush=True)
            labels = [chr(ord("A") + index) for index in range(len(args.arms))]
            blind_order = list(args.arms)
            randomizer.shuffle(blind_order)
            label_to_arm = dict(zip(labels, blind_order, strict=True))
            packet = {
                "case_id": case_id,
                "repeat": repeat,
                "speaker": case["speaker"],
                "listener": case["listener"],
                "gold": case["gold"],
                "test_focus": case["test_focus"],
                "outputs": {
                    label: results[arm] for label, arm in label_to_arm.items()
                },
            }
            write_json(output / "blind" / f"repeat-{repeat}-{case_id}.json", packet)
            mapping[f"repeat-{repeat}-{case_id}"] = label_to_arm
    write_json(output / "blind-mapping.json", mapping)


if __name__ == "__main__":
    main()

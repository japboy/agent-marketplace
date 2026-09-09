#!/usr/bin/env python3
"""Verify local plugin delivery and frozen replay without changing user settings."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile


REPOSITORY = Path(__file__).resolve().parents[2]
DISTRIBUTION_PATHS = (
    Path("apm.yml"),
    Path(".agents/plugins"),
    Path(".claude-plugin/marketplace.json"),
)
TARGETS = (Path(".claude/skills"), Path(".agents/skills"))


def snapshot(root: Path, paths: tuple[Path, ...]) -> dict[str, str]:
    result = {}
    for relative in paths:
        source = root / relative
        files = sorted(source.rglob("*")) if source.is_dir() else [source]
        for file in files:
            if file.is_file():
                result[file.relative_to(root).as_posix()] = hashlib.sha256(
                    file.read_bytes()
                ).hexdigest()
    return result


def run(arguments: list[str], directory: Path, environment: dict[str, str]) -> None:
    result = subprocess.run(
        arguments,
        cwd=directory,
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=180,
        check=False,
    )
    if result.returncode:
        raise AssertionError(
            f"Command failed ({result.returncode}): {arguments!r}\n{result.stdout}"
        )


def verify_skills(consumer: Path, expected: dict[str, bytes]) -> None:
    for target in TARGETS:
        root = consumer / target
        actual = {
            file.relative_to(root).as_posix(): file.read_bytes()
            for file in root.rglob("*")
            if file.is_file()
        }
        if actual != expected:
            missing = sorted(expected.keys() - actual.keys())
            extra = sorted(actual.keys() - expected.keys())
            changed = sorted(
                key for key in expected.keys() & actual.keys()
                if expected[key] != actual[key]
            )
            raise AssertionError(
                f"{target}: missing={missing}, extra={extra}, changed={changed}"
            )


def main() -> None:
    apm = shutil.which("apm")
    if apm is None:
        raise SystemExit("apm is required; run mise install first")
    original = snapshot(REPOSITORY, DISTRIBUTION_PATHS)
    with tempfile.TemporaryDirectory(prefix="agent-marketplace-apm-") as temporary:
        workspace = Path(temporary).resolve()
        publisher = workspace / "publisher"
        consumer = workspace / "consumer"
        consumer.mkdir()
        for relative in DISTRIBUTION_PATHS:
            source, destination = REPOSITORY / relative, publisher / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            if source.is_dir():
                shutil.copytree(source, destination)
            else:
                shutil.copy2(source, destination)
        copied = snapshot(publisher, DISTRIBUTION_PATHS)
        assert copied == original, "Publisher fixture differs from repository"

        catalog = json.loads((publisher / ".claude-plugin/marketplace.json").read_text())
        expected: dict[str, bytes] = {}
        packages = []
        for entry in catalog["plugins"]:
            package = (publisher / entry["source"]).resolve()
            assert package.is_relative_to(publisher), "Plugin source escapes publisher"
            packages.append(str(package))
            manifest = json.loads((package / ".claude-plugin/plugin.json").read_text())
            skills = package / manifest["skills"]
            for skill in sorted(skills.iterdir()):
                if not skill.is_dir() or not (skill / "SKILL.md").is_file():
                    continue
                for file in sorted(skill.rglob("*")):
                    if file.is_file():
                        key = file.relative_to(skills).as_posix()
                        assert key not in expected, f"Duplicate skill file: {key}"
                        expected[key] = file.read_bytes()
        assert packages and expected, "No plugins or skills discovered"

        (consumer / "apm.yml").write_text(
            "name: distribution-test\nversion: 0.1.0\n"
            "description: Isolated plugin delivery test\n"
            "dependencies:\n  apm: []\n"
        )
        environment = os.environ.copy()
        environment.update({
            "APM_HOME": str(workspace / "apm-home"),
            "APM_CACHE_DIR": str(workspace / "apm-cache"),
            "CI": "true",
        })
        run([apm, "pack", "--offline", "--check-clean"], publisher, environment)
        catalog_path = publisher / ".claude-plugin/marketplace.json"
        generated = catalog_path.read_bytes()
        catalog["plugins"][0]["source"] = "./incorrect-source"
        catalog_path.write_text(json.dumps(catalog))
        try:
            drift = subprocess.run(
                [apm, "pack", "--offline", "--check-clean"],
                cwd=publisher, env=environment, capture_output=True, text=True,
                timeout=180, check=False,
            )
            assert drift.returncode == 4, (
                f"Expected catalog drift exit 4, got {drift.returncode}: "
                f"{drift.stdout}{drift.stderr}"
            )
        finally:
            catalog_path.write_bytes(generated)
        # APM 0.30.0 marketplace add writes ~/.apm/marketplaces.json and does
        # not honor APM_HOME. Use the catalog's local sources for this test.
        run([apm, "install", *packages, "--target", "claude,codex"], consumer, environment)
        verify_skills(consumer, expected)
        lock = consumer / "apm.lock.yaml"
        locked = lock.read_bytes()
        for target in TARGETS:
            shutil.rmtree(consumer / target)
        shutil.rmtree(consumer / "apm_modules")
        run([apm, "install", "--frozen", "--target", "claude,codex"], consumer, environment)
        verify_skills(consumer, expected)
        assert lock.read_bytes() == locked, "Frozen install changed the lockfile"
        assert snapshot(publisher, DISTRIBUTION_PATHS) == copied, "Publisher changed"
    assert snapshot(REPOSITORY, DISTRIBUTION_PATHS) == original, "Repository changed"
    print(f"APM delivery verified: {len(packages)} plugins, {len(expected)} files per target; frozen replay passed")


if __name__ == "__main__":
    main()

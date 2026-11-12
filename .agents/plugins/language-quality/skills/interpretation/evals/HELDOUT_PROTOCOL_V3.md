# Prospective temporal-label protocol for interpretation

Use the [V2 protocol](HELDOUT_PROTOCOL_V2.md) and [V2 rubric](RUBRIC_V2.md) with a fresh, unused
fixture. V3 changes only the interpreter prompt's time labels. The earlier speaker utterance is
labeled the **original remark before the listener replied**; the observed `L0` reply and the later
`L1` reply are labeled as subsequent listener turns. The interpreter still receives the same speaker
context, visible listener role and next decision, and natural replies. Listener prompts,
private-information boundaries, frozen grades, outcomes, and acceptance thresholds are V2's.

Run both the raw-only stage and the comparison with `--protocol-v2 --prompt-version v3-temporal`.
Freeze the fixture and gold, Skill snapshots, this note, the V2 protocol and rubric, runner, CLI
version, model, reasoning effort, case IDs, and three repeats before the first model call. Record
their hashes and the prompt version. The raw-run and comparison manifests record `"prompt_version":
"v3-temporal"`; the runner rejects a raw run made under another prompt version before an interpreter
call. Freeze `L0` grades before comparison exactly as V2 requires.

For development replays only, `--prompt-version v3-temporal` can be used without `--protocol-v2`.
That historical-mode path does not freeze `L0` grades or meet this protocol's acceptance gate.

The default `legacy` prompt version retains the historical V1/V2 wording and does not add a
`prompt_version` manifest field. Keep historical results and their frozen runner hashes unchanged.
Do not attribute a difference between a historical V2 run and a new V3 run solely to the Skill:
their prompts and potentially their listener observations differ. Judge a V3 candidate only against
its paired V3 baseline under the same frozen inputs.

# Reproducibility validation

Workflow templates must carry enough metadata requirements for a local agent to write a useful run record.

The validator currently requires every workflow template to declare:

- `reproducibility.record_inputs_hash: true`
- `reproducibility.record_tool_versions: true`
- `reproducibility.record_commands: true`
- `reproducibility.record_environment: true`
- a non-empty `report_template` ending in `.j2`
- an `example_dataset.name`
- either `example_dataset.license` or `example_dataset.status`
- at least one limitation

This is intentionally conservative. A workflow can stay a draft while its example dataset is unresolved, but it must say so with `example_dataset.status`.

## Why this matters

OpenSciFlow workflows should not merely list scientific steps. They should also define what evidence must be recorded before a result is shown to a user.

If a workflow cannot say what inputs, commands, tool versions, environment, citations, and limitations should be recorded, a local agent should not treat it as execution-ready.

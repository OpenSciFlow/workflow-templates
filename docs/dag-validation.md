# DAG validation

Workflow templates describe scientific tasks as ordered steps plus a small dependency graph.

The v0.1 validator checks the parts that can be verified without executing a workflow.

## Step identifiers

Each step must define one of:

- `id`
- `step_id`
- `name`

Current templates use `id`.

## DAG rule

The `dag` object maps each step id to the list of steps it depends on:

```yaml
steps:
  - id: load_inputs
  - id: compute_rmsd
  - id: report

dag:
  load_inputs: []
  compute_rmsd: [load_inputs]
  report: [compute_rmsd]
```

The validator requires:

- every step id appears as a `dag` key;
- every `dag` key is a declared step id;
- every dependency points to a declared step id;
- the graph has no cycles;
- at least one step has no dependencies.

## Why this matters

OpenSciFlow templates are meant to be inspectable before execution. A broken DAG makes it unclear what a local agent should run, what can be skipped, and what artifacts should exist before report generation.

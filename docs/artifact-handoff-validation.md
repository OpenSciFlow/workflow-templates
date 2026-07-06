# Artifact handoff validation

Artifact handoff validation checks whether outputs from one workflow step can satisfy inputs of later steps and final report generation.

The current v0.1 validator checks schema and DAG structure. Artifact handoff validation is the next planned layer.

## Proposed v0.2 step fields

Workflow steps should be able to declare which named artifacts they consume and produce:

```yaml
steps:
  - id: load_inputs
    description: "Load topology and trajectory."
    consumes: ["topology", "trajectory"]
    produces: ["loaded_universe"]

  - id: compute_rmsd
    description: "Backbone RMSD over time."
    consumes: ["loaded_universe"]
    produces: ["rmsd_csv"]
```

Names in `consumes` may refer to:

- top-level workflow `inputs`;
- artifacts produced by dependency steps.

Names in `produces` should refer to:

- intermediate artifacts used by later steps;
- top-level workflow `outputs`.

## Validation rules

The validator should reject a workflow when:

- a step consumes an artifact that is neither a workflow input nor produced by one of its dependencies;
- a final workflow output is not produced by any step;
- two steps produce the same artifact without an explicit merge or overwrite policy;
- a report step does not consume the final scientific outputs it summarizes;
- a step declares outputs that are never consumed and are not top-level workflow outputs;
- a DAG dependency exists only for ordering but no artifact or rationale explains why.

## MD stability target

For `molecular-dynamics-stability-analysis`, the expected handoff is:

| Step | Consumes | Produces |
|---|---|---|
| `load_inputs` | `topology`, `trajectory` | `loaded_universe` |
| `check_quality` | `loaded_universe` | `quality_warnings` |
| `compute_rmsd` | `loaded_universe` | `rmsd_csv` |
| `compute_rmsf` | `loaded_universe` | `rmsf_csv` |
| `compute_rg` | `loaded_universe` | `rg_csv` |
| `report` | `rmsd_csv`, `rmsf_csv`, `rg_csv`, `quality_warnings` | `md_stability_report` |

## Why this matters

Without artifact handoff checks, a workflow can have a valid DAG but still fail at runtime because no step produces the file a later step expects.

For OpenSciFlow, this check is part of moving from a readable workflow template toward an executable local-agent contract.

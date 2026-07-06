# Report template convention

OpenSciFlow reports should be useful to a researcher without overstating what a computational workflow proves.

## Required sections

A report template should include:

1. Task summary.
2. Inputs and input hashes.
3. Workflow template name and version.
4. Plugin manifests and versions.
5. Environment summary.
6. Commands or command-template references.
7. Generated artifacts.
8. Basic quality checks.
9. Citations.
10. Limitations and non-claims.

## Non-claims

Reports must not present workflow output as:

- clinical evidence;
- drug efficacy evidence;
- experimental validation;
- confirmed biological function;
- confirmed binding affinity unless the workflow actually measures or validates affinity.

## Suggested wording

Use direct, bounded language:

```text
This report summarizes a computational workflow run. It records inputs, tools, commands, artifacts, citations, and limitations. The results should be treated as descriptive computational output unless independently validated.
```

Avoid promotional language:

```text
The workflow discovers the mechanism.
The model proves the binder works.
The agent completed the scientific study.
```

## Artifact table

Every report should include an artifact table:

| Artifact | Path | Produced by | Hash | Notes |
|---|---|---|---|---|
| Metrics CSV | `outputs/metrics.csv` | analysis step | `sha256:...` | Descriptive metrics |
| Plot | `outputs/rmsd.png` | plotting step | `sha256:...` | Visualization only |
| Run record | `run_manifest.json` | runner | `sha256:...` | Reproducibility metadata |

## Citations

Reports should carry forward citations from:

- workflow template;
- plugin manifests;
- upstream software;
- model weights or datasets;
- example data source.

If citation metadata is missing, the report should say so instead of inventing one.

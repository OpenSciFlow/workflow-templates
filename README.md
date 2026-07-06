# OpenSciFlow Workflow Templates

Reusable workflow templates for AI for Science tasks, starting with protein-computing workflows.

## What is a workflow template?

A workflow template describes a scientific task as ordered steps or a DAG. It references plugins, declares fallback tools, estimated runtime, hardware requirements, reproducibility metadata, and report templates.

Plugin manifests describe **how one tool/model runs**. Workflow templates describe **how tools are composed into a scientific task**.

## Status

Draft v0.1. These templates are intended for review and iteration.

## Required fields

| Field | Purpose |
|---|---|
| `schema_version` | Template schema version |
| `workflow_name` | Stable workflow identifier |
| `domain` | Scientific domain tags |
| `task_description` | Human-readable task |
| `inputs` | Required/optional inputs |
| `outputs` | Expected artifacts |
| `steps` | Ordered task steps |
| `dag` | Step dependencies |
| `plugins` | Required and optional plugins |
| `fallbacks` | Alternative execution paths |
| `estimated_runtime` | Runtime estimates |
| `hardware` | CPU/memory/GPU requirements |
| `reproducibility` | Metadata that must be recorded |
| `report_template` | Report template path |
| `example_dataset` | Example data information |
| `limitations` | Scientific and technical caveats |

## Initial protein templates

- `protein/protein-ligand-stability.yaml`
- `protein/md-stability-analysis.yaml`
- `protein/mutation-impact-analysis.yaml`
- `protein/ptm-dynamics-analysis.yaml`
- `protein/conformational-ensemble-generation.yaml`

## Review checklist

Short version before merging a template:

- Is the scientific task boundary clear?
- Are inputs and outputs concrete?
- Are required and optional plugins declared?
- Is there a fallback path?
- Is the DAG acyclic?
- Are runtime and hardware estimates included?
- Does the template record reproducibility metadata?
- Is there a report template path?
- Are limitations explicit?
- Does the template avoid overstating computational results as experimental proof?

Full checklist:

- `docs/workflow-review-checklist.md`

Related conventions:

- `docs/report-template-convention.md`
- `docs/example-dataset-policy.md`
- `docs/dag-validation.md`
- `docs/artifact-handoff-validation.md`

## First reference workflow

The first recommended demo workflow is:

```text
molecular-dynamics-stability-analysis
```

It analyzes an existing protein MD trajectory and produces RMSD, RMSF, radius of gyration, plots, a report, and a run manifest.

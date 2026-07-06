# Workflow review checklist

Use this checklist when reviewing a workflow template.

A workflow template should describe a narrow scientific task that can be inspected before execution. It should not ask an agent to invent a research plan from scratch.

## Review outcome

| Outcome | Meaning |
|---|---|
| `needs-scope` | The workflow is too broad or the task boundary is unclear. |
| `needs-plugins` | Required tools/models are missing or not mapped to manifests. |
| `template-valid` | The YAML passes schema validation. |
| `metadata-reviewed` | Inputs, outputs, steps, plugins, fallbacks, runtime, hardware, and limitations have been reviewed. |
| `demo-ready` | A public example dataset and expected artifacts are documented. |
| `report-ready` | The workflow can produce a report with citations, limitations, and run-record metadata. |

## 1. Task boundary

- Is the workflow one repeatable task, not an open-ended research assistant?
- Can a user describe success or failure without interpreting new scientific truth?
- Does the workflow avoid clinical, diagnostic, drug-efficacy, or experimental-validation claims?

## 2. Inputs and outputs

- Are required inputs concrete and checkable?
- Are optional inputs clearly marked?
- Are expected artifacts listed with filenames or file categories?
- Are outputs separated from interpretations and limitations?

## 3. Steps and DAG

- Are steps named and ordered?
- Is the DAG acyclic?
- Does each step have a clear input and output?
- Are manual review points marked where needed?

## 4. Plugin mapping

- Does every automated step point to a plugin manifest or a documented fallback?
- Are required and optional plugins separated?
- Is the minimum acceptable readiness level stated?
- Does the workflow avoid invoking unreviewed shell commands?
- If the workflow uses Slurm or a wrapper script, is the reviewed-wrapper boundary explicit?

## 5. Runtime and hardware

- Are small-demo and typical-run estimates separated?
- Are CPU, memory, GPU, and storage requirements visible?
- Is HPC/Slurm use optional unless the workflow truly requires it?
- If Slurm is used, are account, partition, walltime, module/container, stdout, stderr, and approval requirements visible?

## 6. Reproducibility

- Does the workflow require input hashes?
- Does it record rendered commands and tool versions?
- Does it record model-weight source and checksum when relevant?
- Does it require logs, artifacts, citations, and limitations in the run record?
- For Slurm workflows, does it record job id, rendered `sbatch` command, script path, stdout, stderr, and scheduler metadata?

## 7. Report boundary

- Does the report template include methods, artifacts, citations, and limitations?
- Does it distinguish descriptive computational output from scientific proof?
- Does it tell the user what follow-up validation would be needed?

## 8. Example dataset

- Is the example public, small, and redistributable or easy to regenerate?
- Does the example avoid private, clinical, or sensitive data?
- Are expected artifacts documented without claiming a new discovery?

## 9. Merge rule

Do not merge as `demo-ready` unless a reviewer can name:

- the input files;
- the expected artifacts;
- the plugin manifests used;
- the run-record fields produced;
- the limitations that must appear in the report.

# Protein template review matrix

This matrix summarizes the current internal review state of the protein workflow templates.

It is not an external scientific endorsement. It is a correction-first review aid.

| Workflow | Current structural evidence | Current blocker before demo-ready |
|---|---|---|
| `md-stability-analysis` | Schema-valid, DAG-valid, artifact handoff valid, reproducibility policy declared | Public sample-data license, citation, size, and hashes are not finalized. |
| `protein-ligand-stability-analysis` | Schema-valid, DAG-valid, artifact handoff valid, reproducibility policy declared | Ligand-contact interpretation boundaries and public tiny trajectory policy need review. |
| `mutation-impact-analysis` | Schema-valid, DAG-valid, artifact handoff valid, reproducibility policy declared | Must avoid pathogenicity/function claims; structure-prediction fallback and model-version recording need review. |
| `ptm-dynamics-analysis` | Schema-valid, DAG-valid, artifact handoff valid, reproducibility policy declared | PTM force-field assumptions and paired-input comparability need domain review. |
| `conformational-ensemble-generation` | Schema-valid, DAG-valid, artifact handoff valid, reproducibility policy declared | Generated ensembles must not be presented as equilibrium sampling without validation. |
| `gromacs-rmsd-slurm-analysis` | Schema-valid, DAG-valid, artifact handoff valid, Slurm wrapper boundary declared | Real cluster account, partition, module, stdout/stderr, and approval policy need review. |

## Shared review questions

- Are required inputs narrow enough for a local agent to validate?
- Are final outputs descriptive artifacts rather than unsupported scientific claims?
- Does the report step consume all final outputs needed for interpretation?
- Are fallback paths clear enough that a different tool does not silently change meaning?
- Does the workflow record input hashes, tool versions, commands, environment, citations, and limitations?
- Is the example dataset public, small, and redistributable or regenerable?

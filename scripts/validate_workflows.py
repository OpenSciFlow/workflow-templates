from __future__ import annotations

import json
from pathlib import Path

import jsonschema
import yaml


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schema" / "opensciflow-workflow.schema.json"
PROTEIN_DIR = ROOT / "protein"


def step_id(step: object) -> str | None:
    if not isinstance(step, dict):
        return None
    for key in ("id", "step_id", "name"):
        value = step.get(key)
        if isinstance(value, str) and value:
            return value
    return None


def validate_dag(data: dict) -> list[str]:
    errors: list[str] = []

    steps = data.get("steps", [])
    if not isinstance(steps, list):
        return ["steps must be a list"]

    step_ids: list[str] = []
    for index, step in enumerate(steps):
        current = step_id(step)
        if current is None:
            errors.append(f"steps[{index}] must define id, step_id, or name")
        else:
            step_ids.append(current)

    duplicate_ids = sorted({item for item in step_ids if step_ids.count(item) > 1})
    for duplicate_id in duplicate_ids:
        errors.append(f"duplicate step id {duplicate_id!r}")

    dag = data.get("dag", {})
    if not isinstance(dag, dict):
        return errors + ["dag must be an object mapping step id to dependency list"]

    step_set = set(step_ids)
    dag_set = set(dag)

    for missing in sorted(step_set - dag_set):
        errors.append(f"dag missing step {missing!r}")
    for unknown in sorted(dag_set - step_set):
        errors.append(f"dag references undeclared step {unknown!r}")

    for node, dependencies in dag.items():
        if not isinstance(dependencies, list):
            errors.append(f"dag[{node!r}] must be a list")
            continue
        for dependency in dependencies:
            if dependency not in step_set:
                errors.append(f"dag[{node!r}] depends on undeclared step {dependency!r}")

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str, stack: list[str]) -> None:
        if node in visited:
            return
        if node in visiting:
            cycle_start = stack.index(node) if node in stack else 0
            cycle = " -> ".join(stack[cycle_start:] + [node])
            errors.append(f"dag contains cycle: {cycle}")
            return

        visiting.add(node)
        for dependency in dag.get(node, []):
            if isinstance(dependency, str) and dependency in step_set:
                visit(dependency, stack + [node])
        visiting.remove(node)
        visited.add(node)

    for node in sorted(step_set):
        visit(node, [])

    if step_set and not any(not dag.get(node) for node in step_set):
        errors.append("dag must contain at least one root step with no dependencies")

    return errors


def validate_plugins(data: dict) -> list[str]:
    errors: list[str] = []
    plugins = data.get("plugins", {})
    if not isinstance(plugins, dict):
        return ["plugins must be an object with required and optional lists"]

    for key in ("required", "optional"):
        values = plugins.get(key, [])
        if not isinstance(values, list):
            errors.append(f"plugins.{key} must be a list")
            continue
        seen: set[str] = set()
        for value in values:
            if not isinstance(value, str) or not value:
                errors.append(f"plugins.{key} contains a non-empty string requirement violation")
                continue
            if value in seen:
                errors.append(f"plugins.{key} contains duplicate plugin {value!r}")
            seen.add(value)

    return errors


def artifact_names(values: object, field: str) -> tuple[set[str], list[str]]:
    errors: list[str] = []
    names: set[str] = set()

    if not isinstance(values, list):
        return names, [f"{field} must be a list"]

    for index, value in enumerate(values):
        if not isinstance(value, dict):
            errors.append(f"{field}[{index}] must be an object")
            continue
        name = value.get("name")
        if not isinstance(name, str) or not name:
            errors.append(f"{field}[{index}].name must be a non-empty string")
            continue
        if name in names:
            errors.append(f"{field} contains duplicate artifact {name!r}")
        names.add(name)

    return names, errors


def string_list(value: object, field: str) -> tuple[list[str], list[str]]:
    errors: list[str] = []

    if not isinstance(value, list):
        return [], [f"{field} must be a list"]

    items: list[str] = []
    seen: set[str] = set()
    for index, item in enumerate(value):
        if not isinstance(item, str) or not item:
            errors.append(f"{field}[{index}] must be a non-empty string")
            continue
        if item in seen:
            errors.append(f"{field} contains duplicate artifact {item!r}")
        seen.add(item)
        items.append(item)

    return items, errors


def transitive_dependencies(node: str, dag: dict) -> set[str]:
    dependencies: set[str] = set()
    stack = list(dag.get(node, []))

    while stack:
        current = stack.pop()
        if current in dependencies:
            continue
        dependencies.add(current)
        if isinstance(dag.get(current), list):
            stack.extend(dag[current])

    return dependencies


def validate_artifact_handoff(data: dict) -> list[str]:
    errors: list[str] = []

    steps = data.get("steps", [])
    dag = data.get("dag", {})
    if not isinstance(steps, list) or not isinstance(dag, dict):
        return errors

    workflow_inputs, input_errors = artifact_names(data.get("inputs", []), "inputs")
    workflow_outputs, output_errors = artifact_names(data.get("outputs", []), "outputs")
    errors.extend(input_errors)
    errors.extend(output_errors)

    step_by_id: dict[str, dict] = {}
    for index, step in enumerate(steps):
        current = step_id(step)
        if current is None or not isinstance(step, dict):
            continue
        step_by_id[current] = step

        consumes, consume_errors = string_list(step.get("consumes"), f"steps[{index}].consumes")
        produces, produce_errors = string_list(step.get("produces"), f"steps[{index}].produces")
        errors.extend(consume_errors)
        errors.extend(produce_errors)

        if not consumes:
            errors.append(f"step {current!r} must consume at least one workflow input or upstream artifact")
        if not produces:
            errors.append(f"step {current!r} must produce at least one artifact")

    produced_by: dict[str, str] = {}
    consumed_artifacts: set[str] = set()
    for current, step in step_by_id.items():
        for artifact in step.get("consumes", []):
            if isinstance(artifact, str):
                consumed_artifacts.add(artifact)
        for artifact in step.get("produces", []):
            if not isinstance(artifact, str):
                continue
            if artifact in produced_by:
                errors.append(
                    f"artifact {artifact!r} is produced by both {produced_by[artifact]!r} and {current!r}"
                )
            produced_by[artifact] = current

    produced_artifacts = set(produced_by)
    for missing in sorted(workflow_outputs - produced_artifacts):
        errors.append(f"workflow output {missing!r} is not produced by any step")

    for current, step in step_by_id.items():
        upstream_steps = transitive_dependencies(current, dag)
        upstream_artifacts = {
            artifact
            for artifact, producer in produced_by.items()
            if producer in upstream_steps
        }
        available = workflow_inputs | upstream_artifacts
        for artifact in step.get("consumes", []):
            if isinstance(artifact, str) and artifact not in available:
                errors.append(
                    f"step {current!r} consumes {artifact!r}, but it is not a workflow input or upstream artifact"
                )

    for artifact, producer in sorted(produced_by.items()):
        if artifact not in workflow_outputs and artifact not in consumed_artifacts:
            errors.append(f"artifact {artifact!r} produced by step {producer!r} is never consumed")

    for current, step in step_by_id.items():
        produces = {item for item in step.get("produces", []) if isinstance(item, str)}
        consumes = {item for item in step.get("consumes", []) if isinstance(item, str)}
        is_report_step = "report" in current or any("report" in item for item in produces)
        if not is_report_step:
            continue
        expected_report_inputs = workflow_outputs - produces
        for missing in sorted(expected_report_inputs - consumes):
            errors.append(f"report step {current!r} does not consume final output {missing!r}")

    return errors


def main() -> None:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    files = sorted(PROTEIN_DIR.glob("*.yaml"))
    if not files:
        raise SystemExit("No workflow templates found")

    errors: list[str] = []
    for path in files:
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
            jsonschema.validate(data, schema)
            for error in validate_dag(data) + validate_plugins(data) + validate_artifact_handoff(data):
                errors.append(f"{path.relative_to(ROOT)}: {error}")
        except Exception as exc:  # noqa: BLE001 - report all validation failures clearly.
            errors.append(f"{path.relative_to(ROOT)}: {exc}")

    if errors:
        raise SystemExit("\n".join(errors))

    print(f"Validated {len(files)} workflow templates")


if __name__ == "__main__":
    main()

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
            for error in validate_dag(data) + validate_plugins(data):
                errors.append(f"{path.relative_to(ROOT)}: {error}")
        except Exception as exc:  # noqa: BLE001 - report all validation failures clearly.
            errors.append(f"{path.relative_to(ROOT)}: {exc}")

    if errors:
        raise SystemExit("\n".join(errors))

    print(f"Validated {len(files)} workflow templates")


if __name__ == "__main__":
    main()

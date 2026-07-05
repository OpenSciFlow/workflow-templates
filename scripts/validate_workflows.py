from __future__ import annotations

import json
from pathlib import Path

import jsonschema
import yaml


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schema" / "opensciflow-workflow.schema.json"
PROTEIN_DIR = ROOT / "protein"


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
        except Exception as exc:  # noqa: BLE001 - report all validation failures clearly.
            errors.append(f"{path.relative_to(ROOT)}: {exc}")

    if errors:
        raise SystemExit("\n".join(errors))

    print(f"Validated {len(files)} workflow templates")


if __name__ == "__main__":
    main()


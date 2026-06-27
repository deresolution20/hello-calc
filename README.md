# hello-calc

A tiny Python arithmetic library used to test the agentic build platform end-to-end.

## What this tests

The orchestrator ingests `prd.md`, decomposes it into one Plane task, authors
acceptance tests, spawns a subagent that implements the arithmetic module, and
the PR auto-merges on green CI.

## Development

```bash
pip install -e ".[dev]"
pytest
ruff check src/
mypy src/
```

## Project type

Declared as `library` in `project.yaml`. CI uses GitHub-hosted runners so no
ARC authorization is required on this repo.

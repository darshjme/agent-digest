# Contributing to agent-digest

Thank you for your interest in contributing!

## Getting Started

1. Fork the repository and clone locally.
2. Create a virtual environment: `python -m venv .venv && source .venv/bin/activate`
3. Install in editable mode with test deps: `pip install -e ".[dev]"`
4. Run tests: `python -m pytest tests/ -v`

## Guidelines

- **No external dependencies** — stdlib only (`re`, `collections`, `functools`, etc.)
- **Python 3.10+** — use modern type hints (`list[str]`, `dict[str, int]`, etc.)
- **All new features must have tests** — target 100% coverage for new code.
- **Follow existing code style** — no formatter dependencies required, but keep it clean.

## Pull Request Process

1. Create a branch: `git checkout -b feature/my-feature`
2. Write tests first (TDD preferred).
3. Ensure all tests pass: `python -m pytest tests/ -v`
4. Update `CHANGELOG.md` under `[Unreleased]`.
5. Open a PR with a clear description of what and why.

## Reporting Issues

Open a GitHub issue with a minimal reproducible example.

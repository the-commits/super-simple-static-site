# Contributing to ssss

## Getting Started

```bash
poetry install
poetry build

# Install commit-msg hook (blocks non-Conventional Commits locally)
poetry run pre-commit install --hook-type commit-msg
```

## Running Tests

```bash
# Full test suite with coverage
poetry run pytest --cov=ssss

# Single test function
poetry run pytest tests/test_ssss.py::test_ssss_no_args

# Single test method in a TestCase class
poetry run pytest tests/test_fs.py::Fullpath::test_empty_full_path
```

## Test Coverage

**All new code must have 100% test coverage.** PRs that reduce coverage will not be merged.

- Integration tests go in `tests/test_ssss.py` as plain `pytest` functions. Run the `ssss` CLI via `subprocess` and assert on exit codes and stdout.
- Unit tests go in `tests/test_fs.py` (or a new equivalent file) as `unittest.TestCase` classes.
- Tests must clean up after themselves — remove any files or directories they create.
- No mocking framework. Use subprocess and the real filesystem only.

## Linting

Two flake8 passes are required. The first must produce zero errors:

```bash
# Must be clean — syntax errors and undefined names
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics

# Advisory — style warnings (exit-zero)
flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
```

## Code Style

### General

- Python 3.10+
- Max line length: **127 characters**
- No auto-formatter (black, isort). Follow PEP 8 manually, consistent with existing code.
- No f-strings. Use `+` for string concatenation:
  ```python
  print("Output directory: " + output_dir)
  ```

### Imports

Order: stdlib → third-party → internal (`ssss.*`). Use backslash continuation for long import lines:

```python
from ssss.common.application.variables import application_default_template_path, application_default_template_file, \
    application_default_base_html, application_default_encoding
```

### Type Hints

Add return type hints to standalone functions only. Do not annotate class methods.

```python
def find_config() -> str:
def search_config_in_dir(directory) -> str | None:
def application_config_file_extension() -> list[str]:
```

### Naming

| Kind | Convention | Example |
|---|---|---|
| Modules/packages | `snake_case` | `directory.py` |
| Classes | `PascalCase` | `Application`, `Arguments` |
| Functions | `snake_case` | `find_config`, `get_full_path` |
| Default-value helpers | `application_default_` prefix | `application_default_encoding()` |
| Private instance attributes | double underscore | `self.__config` |

### Class Design

Use inheritance for composition. `__init__` must call `super().__init__()`. Store internal state in double-underscore private attributes.

### Error Handling

Raise built-in exceptions only — no custom exception classes:

```python
raise FileNotFoundError("Config not found: " + path)
raise PermissionError("No write permission: " + directory)
raise NotImplementedError("Must be implemented by subclass.")
```

Lower-level modules raise; they do not print. Catch and print only at the top level in `main()`:

```python
except FileNotFoundError as e:
    print(str(e))
    exit(1)
```

### `__init__.py` Conventions

Each package exposes a clean public API via explicit re-exports. No blank lines between single-line imports:

```python
from .directory import make_empty
from .directory import have_write_permission
from .file import find_config
from .file import touch_if_not_exists
```

## AI Tools Policy

AI coding assistants (Cursor, Copilot, Aider, Claude, OpenCode, etc.) are permitted as productivity aids, but their configuration files, instruction files, and working directories **must not be committed to this repository**.

This is enforced via `.gitignore`. The following are ignored and must stay that way:

- Agent instruction files: `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, `.windsurfrules`, `.clinerules`, `.roomodes`
- Tool directories: `.cursor/`, `.opencode/`, `.claude/`, `.continue/`, `.codeium/`, `.tabnine/`, `.windsurf/`, `.qodo/`, `.plandex/`, `.roo/`, `.smol/`, `.boltnew/`, `.supermaven/`, `.codium/`, `.copilot/`
- Config files: `opencode.json`, `.cursorignore`, `.cursorindexingignore`, `.aider*`, `.github/copilot-instructions.md`

Do not force-add any of these to the repository.

## Pull Requests

Use the pull request template provided. All checklist items must be addressed before requesting review.

## Commit Messages — Conventional Commits

This project uses [commitizen](https://commitizen-tools.github.io/commitizen/) with the Conventional Commits standard. Commit messages drive automatic changelog generation and version bumping — use the correct format.

### Format

```
<type>(<scope>): <subject>
```

`scope` is optional. `subject` is lowercase, no trailing period.

### Types

| Type | When to use | Version bump |
|---|---|---|
| `feat` | New feature | minor |
| `fix` | Bug fix | patch |
| `docs` | Documentation only | none |
| `refactor` | Code restructure, no behaviour change | none |
| `test` | Adding or fixing tests | none |
| `chore` | Build, deps, tooling | none |
| `perf` | Performance improvement | patch |

Breaking changes — append `!` after the type or add `BREAKING CHANGE:` in the footer — trigger a **major** bump.

### Examples

```
feat(md): support frontmatter variables in content files
fix(fs): handle missing config directory on first run
docs: update README with configuration examples
chore(deps): bump pyyaml to 6.0.2
feat!: rename --init flag to --setup
```

### Tooling

```bash
# Interactive commit prompt (guides you through the format)
poetry run cz commit

# Bump version and update CHANGELOG automatically
poetry run cz bump
```


# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

## v1.1.0 (unreleased)

### Added

- `CONTRIBUTING.md` with code style guidelines, 100% test coverage requirement, and AI tools policy
- Pull request template with review checklist
- `CODEOWNERS` — `@the-commits` automatically assigned as reviewer on all PRs
- Branch protection ruleset for `main` and `release/**`: no force push, no deletion, PR + codeowner review required
- `CHANGELOG.md` following Keep a Changelog format
- commitizen for automated changelog generation and version bumping
- `flake8` added as dev dependency so the linter is available in the Poetry virtual environment
- Explicit `jinja2 ^3.1.6` and `zipp >=3.19.1` dependencies to close Dependabot security alerts

### Changed

- Bumped `pyyaml` from `^6.0` to `^6.0.2` for Python 3.14 compatibility
- Bumped `pytest` from `^7.3.1` to `^8.0.0` and `pytest-cov` from `^4.0.0` to `^6.0.0` for Python 3.14 compatibility
- Set `pyproject.toml` version to `1.0.0` to match the published PyPI release

### Fixed

- Dev environment setup now works on Python 3.14
- Resolved 5 Dependabot security vulnerabilities: Jinja2 sandbox breakout (3 CVEs) and zipp DoS

## v1.0.0 (2023-04-19)

### Added

- Initial stable release
- CLI entry point `ssss` with `--init` and `--config` flags
- YAML configuration (`ssss.yml` / `ssss.yaml`) with site-wide variables
- Jinja2 template rendering via `staticjinja`
- Markdown content support with meta variable extraction
- Default file structure generation on `--init`
- Config search order: CWD first, then `~/.ssss/`
- Template naming convention: `__<stem>.j2` per content file, `default.j2` as fallback

[Unreleased]: https://github.com/the-commits/super-simple-static-site/compare/v1.1.0...HEAD
[v1.1.0]: https://github.com/the-commits/super-simple-static-site/compare/v1.0.0...v1.1.0
[v1.0.0]: https://github.com/the-commits/super-simple-static-site/releases/tag/v1.0.0

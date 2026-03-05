# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## v1.2.0 (2026-03-05)

### Feat

- **scaffold**: add --scaffold, --no-seo, --no-sitemap, --no-feed, --no-llm flags
- **scaffold**: add Pico CSS CDN to base.html template
- **cli**: add --version / -v flag
- **ci**: upload coverage to Codecov and add badge to README

### Fix

- **ci**: disable branch ruleset to allow release workflow to push bump commit
- **init**: write starter content into scaffold files on --init
- **ci**: exit gracefully when no commits found for cz bump

## v1.1.0 (2026-03-05)

### Feat

- **ci**: add PyPI publish workflow using Trusted Publishers (OIDC)

### Fix

- **deps**: resolve security vulnerabilities in jinja2 and zipp

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

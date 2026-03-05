# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

### Added

- `--scaffold` flag: runs `--init` implicitly, then writes starter `base.html`, `default.j2`, `index.md`, `sitemap.xml.j2`, `rss.xml.j2`, and `llms.txt.j2`
- `--no-seo` flag: omits Open Graph, Twitter Card, and canonical meta from the scaffolded `base.html`
- `--no-sitemap` flag: skips writing `sitemap.xml.j2` during scaffold
- `--no-feed` flag: skips writing `rss.xml.j2` during scaffold
- `--no-llm` flag: skips writing `llms.txt.j2` during scaffold
- Scaffold files (`base.html`, `default.j2`, `index.md`, `sitemap.xml.j2`, `rss.xml.j2`, `llms.txt.j2`) extracted from Python strings into `ssss/scaffold/` as real files
- `scaffold_directory()` and `read_scaffold_file()` helpers in `ssss.common.application.variables`
- `strip_seo_blocks()` helper strips SEO comment blocks (Canonical, Open Graph, Twitter Card, LLM / AI crawler) from `base.html` when `--no-seo` is used
- `base.html` scaffold includes full SEO meta (Open Graph, Twitter Card, canonical), feed and sitemap autodiscovery, and LLM/AI crawler hints

### Changed

- `--init` no longer writes template and content files — it only creates the config and directory structure
- `confirm_overwrite()` now catches `EOFError` and returns `False` (safe default) for non-interactive use
- Updated `README.md` with full CLI reference, `--scaffold` quick-start, and Pico CSS attribution
- Updated package description in `pyproject.toml`

### Fixed

- `confirm_overwrite()` no longer crashes with an unhandled `EOFError` when stdin is closed (e.g. in CI or subprocess tests)
- Release workflow now temporarily disables the branch ruleset to push the version bump commit directly to main

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

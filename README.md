![example workflow](https://github.com/the-commits/super-simple-static-site/actions/workflows/python-package.yml/badge.svg)
[![codecov](https://codecov.io/gh/the-commits/super-simple-static-site/graph/badge.svg)](https://codecov.io/gh/the-commits/super-simple-static-site)
# Super Simple Static Site (ssss)

ssss is a static site generator that uses Jinja2 and Markdown to build fast, lightweight static HTML sites.
Scaffold a new site in seconds and run it anywhere.

## Installation

### Using uv / uvx (Recommended)

Run `ssss` instantly without manual installation via [uvx](https://docs.astral.sh/uv/):

```bash
uvx ssss --scaffold
```

Or install `ssss` globally as a tool using `uv`:

```bash
uv tool install ssss
```

### Using pipx

Install `ssss` in an isolated environment via [pipx](https://pipx.pypa.io):

```bash
pipx install ssss
```

On Arch Linux, install pipx first if needed:

```bash
sudo pacman -S python-pipx
```

### Using pip

Alternatively, if you are in an active virtual environment:

```bash
pip install ssss
```

## Usage

### Quick start

Run `--scaffold` to initialize a new project, write starter templates and content, and build the site in one step:

```bash
ssss --scaffold
```

This creates:

```
ssss.yml                          # configuration file
site/
  source/
    index.md                      # starter content
    _templates/
      base.html                   # HTML base layout (Pico CSS included)
      default.j2                  # default Jinja2 template
  build/
    index.html                    # generated output
```

### Init only

Use `--init` if you only want to create the configuration file and directory structure, without writing any template or content files:

```bash
ssss --init
```

### Build an existing site

Once a configuration file exists, run ssss without any flags to build:

```bash
ssss
```

### Use a custom config file

```bash
ssss --config path/to/custom.yml
```

## Configuration

Configure your site via `ssss.yml`. The `site` section defines site-wide variables accessible in all templates and content files:

```yaml
site:
  title: My Site
  description: A site built with ssss.
  author: Your Name
  url: https://example.com
```

## Templates

Templates live in `site/source/_templates/`. ssss uses [staticjinja](https://staticjinja.readthedocs.io) for rendering.

- `base.html` — base HTML layout, extended by Jinja2 templates
- `default.j2` — default template, applied to all Markdown files without a dedicated template
- `__<stem>.j2` — template applied only to the content file with the matching stem

The default scaffold includes [Pico CSS](https://github.com/picocss/pico) via CDN — a minimal,
classless CSS framework for semantic HTML that makes every page look clean with zero extra effort.

## CLI reference

```
ssss --help
```

| Flag | Description |
|---|---|
| `--scaffold` | Create config, directories, and starter files, then build |
| `--init` | Create config and directories only |
| `--config`, `-c` | Path to a configuration file |
| `--version`, `-v` | Print the version and exit |
| `--help`, `-h` | Show help and exit |

## License

[AGPL-3.0-or-later](LICENSE) © Magnus Åberg (The Commits)


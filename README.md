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
    blog/
      index.md                    # blog listing
      first-post.md               # sample blog post
    _templates/
      base.html                   # HTML base layout (Pico CSS included)
      default.j2                  # default Jinja2 template
      blog.j2                     # blog template (index + posts)
  build/
    index.html                    # generated homepage
    blog/
      index.html                  # generated blog listing
      first-post.html             # generated blog post
    sitemap.xml                   # automatically generated
    rss.xml                       # automatically generated
    feed.xml                      # RSS alias
    llms.txt                      # LLM-friendly summary
    robots.txt                    # robots directives
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
  email: your@email.com
```

### Per-page frontmatter

Markdown files can include metadata via the Python-Markdown `meta` extension:

```markdown
Title: My Post
Date: 2025-07-29
Description: A short summary.
changefreq: yearly
priority: 0.7
```

These variables are available in templates as `{{ title }}`, `{{ date }}`, `{{ description }}`, etc.
`page_url` (e.g. `/blog/my-post`) is automatically passed for canonical URLs.

## Templates

Templates live in `site/source/_templates/`. ssss uses [staticjinja](https://staticjinja.readthedocs.io) for rendering.

- `base.html` — base HTML layout, extended by Jinja2 templates
- `default.j2` — default template, applied to all Markdown files without a dedicated template
- `__<stem>.j2` — template applied only to the content file with the matching stem
- Subdirectory templates — e.g. `_templates/blog/__index.j2` applies only to `blog/index.md`

The default scaffold includes [Pico CSS](https://github.com/picocss/pico) as a local copy — a minimal,
classless CSS framework for semantic HTML that makes every page look clean with zero extra effort.

### Template variables

Each page receives the following variables during rendering:

| Variable | Source | Description |
|---|---|---|
| `content` | Markdown body | Converted HTML content |
| `title` | Frontmatter `Title` or `<h1>` | Page title |
| `description` | Frontmatter or `site.description` | Meta description |
| `date` | Frontmatter `Date` | Publish date (for RSS) |
| `page_url` | Auto-generated | Canonical path (e.g. `/blog/my-post`) |
| `site` | `ssss.yml` → `site` block | Site-wide variables |

### Blog template

The scaffold includes `blog.j2` which handles both the blog listing (no `date` — shows post list)
and individual posts (has `date` — full article view) using `{% if date %}...{% endif %}`.

## Special files

ssss automatically generates the following files during every build:

| File | Purpose |
|---|---|
| `sitemap.xml` | XML sitemap with per-page `changefreq` and `priority` |
| `rss.xml` / `feed.xml` | RSS feed with `<pubDate>` from frontmatter `Date` |
| `llms.txt` | LLM-friendly site summary (UTF-8 BOM included) |
| `robots.txt` | Robots directives pointing to the sitemap |

Use `--no-sitemap`, `--no-feed`, or `--no-llm` to omit these.

## CLI reference

```
ssss --help
```

| Flag | Description |
|---|---|
| `--scaffold` | Create config, directories, and starter files, then build |
| `--init` | Create config and directories only |
| `--config`, `-c` | Path to a configuration file |
| `--no-seo` | Omit SEO meta tags from scaffold |
| `--no-llm` | Omit `llms.txt` from scaffold and build |
| `--no-feed` | Omit RSS feed from scaffold and build |
| `--no-sitemap` | Omit `sitemap.xml` from scaffold and build |
| `--version`, `-v` | Print the version and exit |
| `--help`, `-h` | Show help and exit |

## License

[AGPL-3.0-or-later](LICENSE) © Magnus "The Commits" Åberg (himself@magnusaberg.me)


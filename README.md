![example workflow](https://github.com/the-commits/super-simple-static-site/actions/workflows/python-package.yml/badge.svg)
[![codecov](https://codecov.io/gh/the-commits/super-simple-static-site/graph/badge.svg)](https://codecov.io/gh/the-commits/super-simple-static-site)
# Super Simple Static Site (ssss)

ssss, short for Super Simple Static Site, is a static site generator that leverages Jinja and Markdown for creating
templates and content. It generates static HTML files for an efficient and lightweight website.

## Installation

The recommended way to install ssss is via [pipx](https://pipx.pypa.io), which installs Python CLI tools in isolated environments and makes them available globally:

```bash
pipx install ssss
```

On Arch Linux, install pipx first if needed:

```bash
sudo pacman -S python-pipx
```

Alternatively, if you are in an active virtual environment:

```bash
pip install ssss
```

## Usage

To initialize a new project, create the default configuration file `ssss.yml`, and build your site, use
the `ssss --init` command. The initialization process also takes care of building the site.

```bash
ssss --init
```

## Configuration

You can configure your site using the `ssss.yml` file. The `site` section allows you to define site-wide variables,
which can be accessed in both content and template files.

```yaml
site:
  title: Super Simple Static Site
  description: A static site generator that uses Jinja and Markdown for templates and content, generating static HTML files.
```

# Super Simple Static Site

ssss or super simple static site, a static site generator, use jinja and markdown as your template and content, and
generate static html files.

## Install

```bash
pip install ssss
```

## Usage

Create a new project with ssss init command, and then you can use ssss build to build your site.

```bash
ssss --init
```

## Configuration

You can configure your site in ssss.yml, and you can use the following variables in your template.

```yaml
site:
  title: Super Simple Static Site
  description: A static site generator, use jinja and markdown as your template and content, and generate static html files.


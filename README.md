# Example README

## File layout

### docs/

Location of markdown docs. File structure determines categories and sections

### docs/assets/css
### docs/assets/javascript
### docs/assets/images
### docs/assets/icons
### docs/assets/glossary
Contains wordlists.

### docs/base_folder_name

Subdirectories of docs become categories. If given a index.md, it will have it's own page.

### docs/summary.md

If using literate-nav provides toc order.

If not supplied then the site will tile all markdown docs out.

### docs/index.md

Landing page. When used in docs subdirectory, will make page as opposed to just a category.

### overrides/

Theme overides or extensions.

### custom_hooks.py

Custom hooks.
    - on_env : Injects application info from 'module-list' into jinja build env.
    - lint -> moved to CI
    - link_checker -> moved to CI

## Theme

https://squidfunk.github.io/mkdocs-material/


## Setting up a local development environment

First time setup

```sh
git clone <path to repo>
cd <name of repo>
pip install -r requirements.txt
```

Build

```sh
mkdocs serve
```

Then browse to http://localhost:8000/

## Contributing

We welcome contributions to our User Guides. Please read [CONTRIBUTING.md](CONTRIBUTION.md)

## Formatting

See [docs/format.md](docs/format.md)

## Build filters

These are filters that should be run whenever a page is edited.

Currently triggered in CI
    - proselint
    - mdspellcheck

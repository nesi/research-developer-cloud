# Example README

## File layout

### docs/

Location of markdown docs. File structure determines categories and sections

### docs/assets

This is broken down into a few things, treat this as site assets like `css`, `images` or `files(pdfs etc)`

### docs/base_folder_name

Subdirectories of docs become categories. If given a index.md, it will have it's own page.

### summary.md and index

These 2 files are used as the following

`index.md` is the base page for that section or group

`summary.md` is the nav structure for that section or group, if not supplied then the site will tile all markdown docs out

### overrides/

Theme overides or extensions.

### custom_hooks.py

Custom hooks.
    - on_env : Injects application info from 'module-list' into jinja build env.
    - lint -> moved to CI
    - link_checker -> moved to CI

## Theme

https://squidfunk.github.io/mkdocs-material/

## Contributing

We welcome contributions to our User Guides. Please read [CONTRIBUTING.md](CONTRIBUTION.md)
Pages hosted [here](https://cwal219.pages.hpcf.nesi.org.nz/mkdocs).

### Build filters

These are filters that should be run whenever a page is edited.

Currently triggered in CI
    - proselint
    - mdspellcheck

Currently Being run through mkdocs:
    - Spellcheck
    - Dead link checker

Would be better to run these independently so they can be run by gitlab CI.
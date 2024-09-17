# NeSI docs template

Put some infor about the site here.

## Contents

The repository is organised using the following folders:

- `checks` : scripts intended to be run by CI,
- `docs`: markdown files, structure determines categories and sections[^1],
- `docs/assets`: non-template related files, e.g. images,
- `overrides`: theme overides or extensions for page templates.
- `overrides/partials`: Overrides and extensions for sub components.

[^1]: A section or category can be replaced by an `index.md` file, this will replace the default nav with a page.

## Developer Documentation

Following pages contain information to help maintain the documentation:

- See [contributing](https://nesi.github.io/support-docs/CONTRIBUTING) ([local version](docs/CONTRIBUTING.md)), to learn how to you can contribute.
- See [formatting](https://nesi.github.io/support-docs/FORMAT), for examples of markdown syntax.
- See [create a new page](https://nesi.github.io/support-docs/NEWPAGE), for general principles to consider when writing pages.
- See [macros](https://nesi.github.io/support-docs/MACROS), for `mkdocs-macros-plugin` environment.
- See [checks](checks/README.md), for information on quality assurance tests.
- See [workflows](.github/workflows/README.md), for information on CI workflows.

## Viewing PR Branches

![Demo Site](https://github.com/CallumWalley/support-docs-dev/actions/workflows/deploy.yml/badge.svg)

Deployments of open pull requests can be viewed at [https://callumwalley.github.io/support-docs-dev/NAME-OF-BRANCH](https://callumwalley.github.io/support-docs-dev/)

## Theme

We are using the [mkdocs material theme](https://squidfunk.github.io/mkdocs-material/).

## Analyics

Google Analytics can be set up.
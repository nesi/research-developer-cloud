# NeSI docs template

Replace this readme with info about the site.

## First Time Setup

You will need to have Python **3.10** or later installed on your computer.

Clone this repository and create a Python virtual environment using:

```sh
git clone https://github.com/nesi/nesi-mkdoc-template.git
cd nesi-mkdoc-template
python -m venv .venv
source .venv/bin/activate
pip3 install pip-tools
pip-compile
pip3 install -r requirements.txt
```

## Build and deploy

```sh
source .venv/bin/activate
mkdocs serve -c
```

Take note of any warnings or errors.

A link to the deployment will be printed once served.

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

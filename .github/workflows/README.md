# CI

Description of current CI workflow.

## [checks.yml](checks.yml)

A series of QA checks run on the documentation.

The checks can be started manually from the ![workflow page](https://github.com/nesi/<repo-name>/actions/workflows/checks.yml/badge.svg),
select the target branch, give the pattern of files to include, and select which checks you want done.

Checks will also be run on any _non main_ branch pushes. All checks will be run, but only on _changed_ files.

More info on what these checks do in [README.md](../../checks/README.md)

## [deploy.yml](deploy.yml)

Runs on push to _main_ branch. Builds and deploys pages.

## [depo_deploy.yml](demo_deploy.yml)

## [auto_merge.yml](auto_marge.yml)

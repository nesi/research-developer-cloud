# SETUP

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

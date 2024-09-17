"""
mkdocs_hooks allows injection of variables into templating stage of rendering.
This allows for arbitrary use of variables in TEMPLATE FILES, (e.g. `overrides/*.html`).
As opposed to `macro_hooks.py` which injects variables into macro rendering (e.g. `docs/*.md`).
If this is confusing, ask Cal to explain.
"""

# Allows the use of {{ FOO }} variable in `overrides/*.html`.

# def on_env(env, config, files, **kwargs):
#     env.globals["FOO"] =  "BAR"

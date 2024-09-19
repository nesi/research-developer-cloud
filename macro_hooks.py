"""
Allows injection of variables into macro stage of rendering.
This allows for arbitrary use of variables in ARTICLES, (e.g. `docs/.md`).
As opposed to `mkdocs_hooks.py` which works only in template step, (e.g. `overrides/*.html`).
If this is confusing, ask Cal to explain.
"""

# Allows the use of {{ FOO }} variable in `docs/*.md`.


def define_env(env):
    """
    This is the hook for defining variables, macros and filters

    - variables: the dictionary that contains the environment variables
    - macro: a decorator function, to declare a macro.
    - filter: a function with one of more arguments,
        used to perform a transformation
    """

#     # add to the dictionary of variables available to markdown pages:
#     env.variables.foo = "bar"
    return


# def on_pre_page_macros(env):
#     return


# def on_post_page_macros(env):
#     return


# def on_post_build(env):
#     return

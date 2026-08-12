# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

Content-only MkDocs Material site for the NeSI / REANNZ **Research Developer Cloud** (RDC), an
OpenStack platform. Published to <https://support.cloud.nesi.org.nz/> via GitHub Pages. There is no
application code here — the "source" is Markdown in `docs/`, plus a small Python toolchain that
lints it and builds the site.

Almost every change is a documentation change. Treat prose quality and voice as the primary concern,
and the build config as secondary.

## Commands

```sh
pip install -r requirements.txt     # full pinned toolchain (pip-compile from requirements.in)
mkdocs serve                        # local preview at http://localhost:8000/
mkdocs build --clean                # writes to public/ (site_dir), not site/
```

QA checks. Each takes a space-delimited file list; pass `docs/**/*.md` to lint everything. CI runs
these on changed files for any push to a non-`main` branch.

```sh
python3 checks/run_spell_check.py docs/path/to/page.md   # pyspelling + aspell, needs `apt install aspell`
python3 checks/run_proselint.py   docs/path/to/page.md
python3 checks/run_meta_check.py  docs/path/to/page.md   # frontmatter + heading rules
markdownlint --config .markdownlint.json --json docs/path/to/page.md 2>&1 | python3 checks/parse_markdownlint.py
./checks/run_test_build.py                               # strict-ish build, surfaces mkdocs warnings
```

Checks also have VSCode debug jobs (`.vscode/tasks.json`), most of which run against
`checks/fail_checks.md` — a deliberately broken page used as a fixture. Don't "fix" it.

Deploy is automatic on push to `main` (`.github/workflows/deploy.yml`). Never build to `gh-pages` by
hand.

## Architecture

**Nav is not in `mkdocs.yml`.** It comes from `mkdocs-awesome-nav` reading `.pages.yml` files
scattered through `docs/`. To place a new page or section, edit the `.pages.yml` in its parent
directory. A trailing `- "*"` means "then everything else, alphabetically". An empty `.pages.yml`
(e.g. `docs/user-guides/set-up-your-cli-environment/`) leaves that folder's ordering to the plugin.
Directory structure defines sections; `index.md` is that section's landing page.

**Two hook files, easily confused:**

- `macro_hooks.py` → `define_env()`, injects variables usable in **Markdown** via `{{ ... }}`
  (mkdocs-macros). Currently exposes `applications` from `docs/assets/module-list.json`.
- `mkdocs_hooks.py` → injects variables into **Jinja templates** in `overrides/*.html`.

Because mkdocs-macros processes every page, literal `{{ }}` in a code block must be wrapped in
`{% raw %}` / `{% endraw %}` or the build fails (`on_error_fail: true`). See
`docs/user-guides/create-and-manage-keypairs/rotate-ssh-keys.md` for the one existing example.

**Externally-managed assets.** `docs/assets/glossary/dictionary.txt` and `docs/assets/module-list.json`
are pulled in by CI from the `nesi/nesi-wordlist` and `nesi/modules-list` repos. Do not hand-edit the
dictionary to silence a spellcheck failure — fix the spelling, or raise it upstream.

`redirect_map.yml` exists but the `redirects` plugin is **not** enabled in `mkdocs.yml`. Renaming or
moving a page currently breaks its published URL; call that out rather than assuming a redirect
catches it.

## Page conventions

Frontmatter, as enforced by `checks/run_meta_check.py`:

```yaml
---
hidden: false
label_names:      # at least one; the vocabulary is checks/.approved_tags.yml
- keypairs
- security
position: 1
title: Create and Manage Keypairs      # ≤ 28 chars, title case
description: One sentence, used in search results and cards
---
```

`index.md` files are exempt from the meta checks, which is why many carry no `description`.

Other conventions:

- Code fences carry a language attribute: `` ``` { .sh } `` for commands, `` ``` { .sh .no-copy } ``
  for output the reader should not copy. The `.no-copy` variant is the more common of the two.
- Cross-page links are relative and point at the `.md` file, not the built URL.
- Callouts use `!!! note` for context and caveats. `!!! warning` is rare — reserve it for genuinely
  destructive actions (data loss, lockout). Most pages have zero; the corpus norm is at most two.
- New Zealand English throughout (organisation, authorised, visualisation).
- Support address is `support@cloud.nesi.org.nz`.

**Naming is inconsistent and it is not your job to fix it wholesale.** The platform is called
"FlexiHPC" on ~123 lines and "RDC" / "Research Developer Cloud" on ~28. Newer pages prefer RDC. Match
the page you are editing; don't rename across the repo without being asked.

## Voice

This is the part most likely to go wrong. The house style is **descriptive and permissive** — explain
what a thing is and what will happen, then let the reader decide. It reads as a platform team sharing
what it knows, consistent with the shared-responsibility framing in `docs/security/`.

Characteristic constructions:

- "You **are able to** create a new SSH Key pair on the RDC or import one of your own."
- "Key pairs **can be** managed a few ways"
- "This **allows you to** adopt the principle of least privilege"
- "You **will need to** ensure you have created and assigned a Security group"

Bare imperatives are fine *inside* a numbered step the reader has already committed to ("Copy the
floating ip address", "run the following command"). They are out of place in prose about choices.

Avoid:

- Policy vocabulary — "never", "do not", "you must", "grant access to the smallest group".
  NeSI documents the platform; it does not write the reader's internal policy.
- Headings that grant or withhold permission ("Who may hold the secrets"). Name the topic instead.
- Instructions about the reader's organisation or calendar — "on their last day", "at least once a
  year", "record what was rotated".
- Conduct checklists. Tables here carry reference data (flavours, default users, image formats), not
  rubrics.
- A more literary register than the surrounding pages. The corpus is plain and workmanlike.

The reliable transform is **prescription → consequence**: instead of "Set a passphrase on every
private key", write "A private key with a passphrase is useless to anyone who copies the file", and
let the reader draw the conclusion.

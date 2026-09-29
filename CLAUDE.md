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

Pages under `docs/` follow this section, not Writing Style below. Writing Style governs the
repo's own contributor docs (`README.md`, `CONTRIBUTION.md`, this file), pull request
descriptions, and Jira issues. Where the two disagree on a page under `docs/`, this section
wins.

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

<!-- anchor:start:workflow -->
## Workflow

Work is tracked as **Jira issues in the HPC project** on `https://reannz.atlassian.net`. One
issue can cover work across several repos, so the issue names which repos it touches rather
than living inside one of them.

This section governs changes made by the HPC team and by agents working in this repo. Other
contributors open pull requests from branches of their own naming, some keyed to other Jira
projects, and are not held to it. Leave their branches and pull requests as they are.

### Prerequisite: the Atlassian MCP Server

Everything below runs through a self-hosted `mcp-atlassian` server. It is per-machine
configuration, not something this repo ships, and the Jira tools do not exist without it.
Confirm it before starting work rather than when the first tool call fails:

```bash
claude mcp list      # the atlassian line must read: ✔ Connected
```

If that line reports `CONNECTION_CLOSED`, re-run it with the sandbox disabled before changing
any config. `uvx` needs to write a lock file under `~/.cache/uv`, that path is read-only
inside the sandbox, and the spawn dies before the server starts. The failure is an artifact
of where the check ran, not a broken setup.

If the server is genuinely absent, see
`docs/solutions/workflow-issues/atlassian-mcp-self-hosted-setup.md` in the `agent-claudesmith`
repo for the env file, the `~/.claude.json` entry, and the API token. Do not work around a
missing server by editing issues in the browser and leaving the repo out of step; fix the
server.

### Work Starts From a Jira Issue

The issue is the spec. Not a chat message, not a scratch note: the issue. This is what lets
an engineer or an agent pick work up cold, in a fresh session with no conversation history,
and still know what done means.

If you are asked to build something and no issue exists, create it first and get it agreed
before touching code. An issue is ready to be picked up when its description carries all of:

- **Goal** — one or two sentences on what the change achieves.
- **Decisions already made** — the settled choices, so the next person does not reopen them. Say what was chosen, not what was considered.
- **Scope** — explicitly in and explicitly out. The out list matters more; it is what stops the work sprawling.
- **Epic** — the repo epic this sits under, by key and name. One epic only, the repo where the change principally lands. It is set in the `parent` field; the description line just records the choice.
- **Repositories** — every repo the work touches, by full path, for example `nesi/research-developer-cloud`. Jira has no notion of where the code lives, so this list is the only record.
- **Acceptance criteria** — a checklist where each line is individually demonstrable as true or false. "The page reads better" is not one. "`/docs/getting-started` returns 200 and contains the new install block" is.
- **Test plan** — which command runs, and what it asserts. See the QA checks under Commands above.

Create and read issues through the Atlassian MCP tools, all prefixed
`mcp__atlassian__`: `jira_create_issue`, `jira_get_issue`, `jira_update_issue`,
`jira_search`, `jira_transition_issue`, `jira_add_comment`. Discover ids rather than
guessing them: `jira_get_transitions` for transition ids, `jira_get_create_fields` for
what a project's issue type requires, `jira_get_link_types` before `jira_create_issue_link`.
No Jira CLI is installed on this machine.

Issue descriptions are written in **Markdown**; the server converts them to Jira wiki
markup on the way in, because `HPC` is a classic project. Do not hand-write
wiki markup. Two traps, both found the hard way:

- **Never put a `|` inside a Markdown table cell**, not even inside backticks. It breaks the
  table, the converter gives up, and your raw Markdown is stored verbatim — which a classic
  project renders literally, `##` and all. Rephrase the cell instead.
- **Markdown checkboxes do not survive.** `- [ ]` and `* [ ]` both come out as plain bullets.
  Track completion in the PR, or type the boxes in the Jira UI, which stores what you type
  without conversion.

After creating or editing a description, read it back and confirm it converted. A silent
fallback looks fine in the tool response and wrong in the browser.

If the design changes while you are implementing, edit the issue rather than letting it
drift. A stale issue is worse than none, because it asserts something that is no longer true.

**Classification:** set a Jira **label** for each area touched (`docs`, `ci`) and for the
repo (`research-developer-cloud`). Labels, not components: on this tenant
`project = HPC AND component IS NOT EMPTY` returns zero issues project-wide.

**Every issue sits under a repo epic.** The HPC project's epics are named after
repositories, not themes, and the epic summary is the **bare repo name**, not the full forge
path. This repo's epic is `HPC-801`. An issue that touches several repos still gets
exactly one epic — the repo where the change principally lands — and the others stay in the
issue's Repositories list; do not clone the issue per repo. If the repo you are working in
has no epic yet, create one before the issue: issue type **Epic** (id
`10567`), summary the bare repo name. **Do not file new work under any epic
that is not named after a repository.** The epics that predate this convention are not
maintained against it, and several are still In Progress, so they look like live homes for
new work. The test is the epic's summary, not its status: if it is not a repo name, it is not
the target.

### Before Making Changes

1. Read the issue in full: `jira_get_issue` with the key, for example `HPC-123`.
2. Transition it to **In Progress** (transition id `21`) so the board reflects reality.
3. Put the issue on the board properly. It must sit under its **repo epic**, in the
   **current sprint**, and carry an **assignee**. Set whichever is missing before writing
   code. Work in flight that is absent from the sprint makes the board lie about what the
   team is doing, and people plan from the sprint, not from the issue list. An in-progress
   issue with no assignee has the same defect: nobody can tell who holds it. An issue with
   no epic is invisible in the only view that shows one repository's work on its own. All
   three apply to an issue you created a minute ago, because creating an issue neither adds
   it to a sprint, nor assigns it, nor parents it unless you pass the field.

   No agile MCP tool is enabled, so the sprint is an ordinary field. Look up the open sprint
   with JQL, then write its **numeric id**, not its name, to `customfield_10020`. The epic
   goes in `parent` as a plain issue key, and the assignee in the same call:

   ```
   jira_search       jql "project = HPC AND sprint in openSprints()" \
                     fields "customfield_10020"

   jira_update_issue issue_key HPC-123 \
                     fields '{"parent": "HPC-801", "customfield_10020": <open sprint id>, "assignee": "you@reannz.co.nz"}'
   ```

   On `jira_create_issue` the same three go in `additional_fields`, except `assignee`, which
   is its own top-level argument.

   **The field is `parent`, not "Epic Link".** `customfield_10014` ("Epic Link") is still
   defined on the tenant, but it is off the HPC screens and empty on every
   issue — an issue that sits under an epic has `parent` set and `customfield_10014` absent.
   So a JQL `"Epic Link" IS EMPTY` matches the whole project and cannot be used to find
   issues that are genuinely missing an epic. `parent IS EMPTY` is the query that works —
   exclude the epics themselves, which have no parent by definition. Look a repo's epic up
   by summary rather than trusting a key copied out of these instructions:

   ```
   jira_search       jql "project = HPC AND issuetype = Epic AND summary ~ 'research-developer-cloud'"

   jira_search       jql "project = HPC AND issuetype != Epic AND parent IS EMPTY"
   ```

   Assign to the account the MCP server authenticates as, which is `JIRA_USERNAME` in its env
   file. An email works as the identifier, and so does an account id.

   **Look the sprint id up every time.** The example above carries a placeholder rather than a
   number on purpose: sprints roll over roughly fortnightly, so any id written here is stale
   within a fortnight, and `2482` — HPC Sprint 8, which ended 2026-09-03 — is what copying one
   out of these instructions gets you. `customfield_10020` is the Sprint field for this tenant
   rather than for this repo; confirm it with `jira_search_fields` on the keyword `sprint` if a
   write is rejected.

   Read all three fields back afterwards. A wrong sprint id is accepted silently and puts the
   issue on another team's board, and a `parent` that was dropped leaves the issue off its
   repo epic — `jira_update_issue` reports success either way.

   Keep the repo **label** as well (`research-developer-cloud`, alongside the area labels under
   Classification above). The epic did not replace it: an issue carries both, and the label
   is what a plain `labels = research-developer-cloud` search matches.
4. Base the work off `main`. It is the integration base for this repo.
5. Review the existing implementation before modifying it. No blind edits.
6. Preserve existing behaviour unless the issue requires changing it. Do not fold unrelated refactors into the diff; open a separate issue instead.

### Branches and Commits

Branches carry the Jira key first: `HPC-123-<slug>`. The key in the branch name and the pull
request title is what the GitHub for Jira app matches to populate an issue's development
panel. Whether that app is connected to this repo, and whether it also links keys in commit
messages, is unverified: check the development panel of the first HPC issue whose pull request
lands here, then replace this sentence with what it shows.

Commits follow Conventional Commits with a scope, and name the key in the body. One logical
change per commit; never mix a refactor into a feature.

### Deliverable

The deliverable is a pull request into `main`, not a set of local commits. Run
the QA checks under Commands above on the files you changed before you push, then:

```bash
git push -u origin HPC-123-<slug>

gh pr create --base main --template hpc.md \
  --title "HPC-123: <what the change does>"
```

The PR description must **name the issue** as a full link,
`https://reannz.atlassian.net/browse/HPC-123`, and **walk the acceptance criteria** from the
issue, each marked met or not met. An unmet criterion is a conversation, not something to
drop quietly. Merging the PR will not move the issue. No Jira automation is configured to
do it, so transitioning is a manual step you own.

Never mark a criterion met that you have not observed.

### Finishing

Once the PR is merged, transition the issue to **Done** (transition id
`31`) and edit the description so it reflects what was actually built.
Nothing does this for you.

**HPC transition ids:** To Do `11`, In Progress `21`, In Review `2`, On Hold `3`, Done `31`, NOT DONE `4`

**Agent rule:** do not declare a task done until the issue exists, the checks pass, the PR
is open, and the issue has been transitioned. Anything short of that is work in progress.
<!-- anchor:end:workflow -->

## Writing Style

Follow this convention whenever you are writing a document such as a README.md or similar for
a coding project, or when I ask you to write documentation.

Technical design or discovery documents should be written as if they are intended for future
engineers who need to understand a system quickly. Preserve all technical findings,
evidence-based conclusions, risks, assumptions, decisions, and open questions. Do not preserve
reasoning process, investigative journey, rhetorical style, speculation history, or
conversational commentary unless it materially affects the final conclusions.

Prefer:

- concise declarative statements
- executive-summary-first structure
- clear separation of evidence, conclusions, decisions, and open issues
- tables over prose where appropriate
- operational clarity over narrative flow

Avoid:

- rhetorical questions
- conversational asides
- "this is interesting"
- "this suggests"
- "most likely"
- "worth noting"
- meta commentary about previous versions of the same document, or assumptions that are no
  longer referenced in the current version (other than when we're documenting the why or the
  rationale about a design choice)
- repeated revisiting of the same conclusion
- investigator-style thought progression

Write in the style of an experienced systems engineer producing handover documentation for
another engineer six months from now.

### Scope

| Governs | Does not govern |
|---|---|
| READMEs, design and discovery documents, runbooks, ADRs, postmortems, MR descriptions, Jira issue descriptions, commit message bodies | Code identifiers, log lines, JSON and YAML keys, test names, error strings emitted by code, generated output |

Short content — a commit subject, an error message — takes only the first four rules below.
Typography and structure rules add nothing at that length.

Two rules resolve the conflicts this section would otherwise create:

- **Tables for reference material, prose for connected argument.** "Tables over prose" applies
  to anything a reader scans for one value. A chain of reasoning fragmented into bullets loses
  the links between its steps. A two-sentence bullet means you needed a paragraph.
- **When a rule fights the sentence, drop the rule.** Style serves clarity, never the reverse.
  Deviating is a judgement call, not a violation to flag.

### Sentence Rules

Apply these while writing, not as a pass afterwards.

**Active voice unless the actor is genuinely unknown.** Passive voice deletes the actor, which
is the fact a handover document exists to record.

- BAD: `The incident was caused by a misconfigured load balancer rule.`
- GOOD: `A typo in the ingress-nginx path-rewrite regex routed /auth/* to the wrong upstream.`

**Attach a number to every claim of improvement, regression, or scale.** Without one the reader
cannot verify the claim or reproduce the measurement.

- BAD: `The new image builds significantly faster.`
- GOOD: `The image builds in 11 minutes, down from 26 (packer build, 3 runs, warm cache).`

**Cite the evidence or admit its absence.** "Industry best practice", "studies show" and
"everyone agrees" are unverifiable. Where you have no source, say the claim is unverified and
name what would settle it.

- BAD: `Best practice is one minor version per upgrade hop.`
- GOOD: `Upgrade one minor version per hop; skipping versions is unsupported by kubeadm (see the Kubernetes version-skew policy). Unverified for CAPO provider upgrades — confirm against the CAPO release notes before relying on it.`

**Replace category words with the specific items.** `factors`, `aspects`, `considerations`,
`elements`, `issues`. Reaching for one means the specifics are still missing.

- BAD: `Several factors affect upgrade reliability.`
- GOOD: `Upgrade reliability depends on etcd snapshot age, MachineTemplate immutability, and whether the control plane has spare capacity for a surge node.`

**Cut needless words.** "In order to" is "to". "At this point in time" is "now". "It should be
noted that" is deletable entire.

**No em-dash or en-dash as casual punctuation.** Use a comma, parentheses, a period, or rewrite.
Reserve the em-dash for a genuine aside where parentheses read wrongly.

**Drop "Additionally", "Furthermore", "Moreover".** These are throat-clearing. Delete the
connector, or replace it with one that carries meaning: "Even so", "By contrast",
"The exception:".

**Do not close a section with a summary of that section.** The reader has just read it. Close
with a consequence, an open question, or a pointer to the next thing.

**Hold one term per concept.** If the document says "rollback", it does not later say
"rolling back", "the rollback process", or "reversion". Renaming a thing mid-document reads as
a second thing.

**Keep coordinate ideas parallel.** `The pipeline detects, identifies, and fixes`, not
`The pipeline detects, will identify, and is going to fix`.

**Split sentences over about 30 words, and vary their length.** Uniform sentence rhythm is the
clearest signal that nobody edited the text.

### Before Declaring a Document Done

- Every improvement, regression, or scale claim carries a number.
- Every non-obvious claim carries a citation, or says it is unverified.
- Active voice throughout, except where the actor is genuinely unknown.
- No em-dash habit, no "Additionally", no section that closes by summarising itself.
- Decisions, risks, assumptions, and open questions each appear somewhere a reader can find
  them without reading the whole document.
- Nothing remains that narrates how the document was researched.

<!--
The eleven sentence rules are a document-focused subset of the 21 in `agent-style`, condensed
from [yzhao062/agent-style](https://github.com/yzhao062/agent-style) v0.3.1, CC BY 4.0. They
correspond to RULE-02, 03, 04, 08, 09, 12, B, D, E, F and H, plus RULE-A inside the tables-vs-prose
tiebreak. Keep this credit line if you copy the section onward.
-->

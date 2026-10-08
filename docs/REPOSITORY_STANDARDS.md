# Repository Standards

What a reader should be able to do in any Know repository within five minutes:
understand what it is, run it, test it, and know where to report a problem.

These are defaults, not a template to be applied mechanically. A Rust runtime, a
Vite site, a Python service, and a research repository are genuinely different;
standardize the parts that reduce confusion, and keep the differences that
reflect the technology.

## Required for every repository

| Artifact | Rule |
|---|---|
| `README.md` | Present, at the root, in English. Structure below. |
| Default branch | Named `main`, protected once the repository has more than one contributor. |
| CI | Runs on every pull request; the commands it runs are the same ones the README documents. |
| Security reporting | The repository's `SECURITY.md`, or the organization default from this repository. |
| No secrets | Ever. `.env`-style files are ignored, and fixtures use obviously fake values. |
| License | Explicit, once the repository is public. Private repositories may defer this decision, but not forever. |

Community files (`CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, issue templates) come
from this organization's `.github` repository by default. A repository needs its
own copy only when its process genuinely differs; in that case the local file
wins, so keep the difference intentional.

## Recommended README structure

```markdown
# <repository name>

One paragraph: what this is, what problem it solves, and what it deliberately
is not. No marketing language.

## Status
Stage and honesty: prototype / in development / maintained / archived.
What works, what does not, what is not claimed.

## Requirements
Runtimes and versions actually needed (Python 3.12+, Node 22, Rust stable).

## Setup
The exact commands, in order, that work from a clean clone.

## Usage
How to run it. What you should see.

## Development
- Test: <exact command>
- Lint / typecheck: <exact command>
- Build: <exact command>

## Configuration
Every environment variable or config key: purpose, default, and whether it is
public or secret. Table, not prose.

## Architecture
Short description plus a pointer to `docs/architecture.md` or a diagram if the
system deserves one.

## Documentation
Links to the deeper documents, each with one line about what is in it.

## Contributing / Security
One line each, linking to CONTRIBUTING.md and SECURITY.md.
```

Skip sections that do not apply rather than filling them with "N/A".

### Honesty rules for READMEs

- Describe what a fresh clone can actually do today.
- Never describe a planned feature in the present tense.
- Distinguish *works on my machine* from *verified by CI* from *deployed*.
- If a step is Windows-only, macOS-only, or platform-specific, say so in the
  step, not in a footnote.

## Development commands

Document the real commands the project uses, not aspirational ones:

- One command to install, one to run, one to test, one to build.
- Prefer the tool the repository already uses (uv, npm, cargo, make) over a new
  wrapper script.
- If a command takes minutes or needs network access, say that next to it.
- Commands in the README must have been run by the person who wrote them.
  A README command that fails on a clean clone is a bug, file it.

### Environment configuration

- Ship a complete `.env.example` (or equivalent) with every variable the
  application reads, dummy values only.
- Never place a real secret in an example file, a test, a fixture, or a
  screenshot.
- Classify every variable as public or secret. Anything exposed to browser code
  is public, whatever prefix it carries.

## Testing

- Every repository has a documented test command; if it has no tests, the
  README says so and why.
- Tests are deterministic. No network-dependent assertions, no reliance on
  wall-clock timing, no order dependence between tests.
- Tests never touch real user data or production credentials, they build
  their own temporary state.
- CI runs the test suite on every pull request. A repository whose tests only
  run on one machine has not got tests; it has got a ritual.

## Documentation

- Documentation lives next to the code it describes; deep reference material
  belongs in `docs/`.
- Architecture documents state their date and the commit they describe.
- Decision-making that will matter later gets an ADR: see
  [adr/README.md](adr/README.md).
- Diagrams: source format in the repository, so the diagram can be edited;
  images exported, not only screenshotted.

## Changelogs and releases

- Until a repository publishes releases, the pull request history **is** the
  changelog: write pull request titles a future reader can search.
- When a repository starts publishing releases, use an explicit `CHANGELOG.md`
  (Keep a Changelog format is fine) or generated release notes, and do both
  consistently.
- Release notes describe user-visible behaviour, not commit hygiene.

## Continuous integration

Baseline for a new repository: pick the workflow template in
[`workflow-templates/`](../workflow-templates/) that matches the stack:

1. Checkout, pinned to a commit SHA.
2. Install dependencies from the lockfile.
3. Lint and typecheck.
4. Tests.
5. Build.
6. Dependency and credential audit.

Rules that apply to every workflow in the organization: least-privilege
`permissions`, no secrets exposed to untrusted pull requests, no automatic
production deployment, no automatic merging. See
[SECURITY_BASELINE.md](SECURITY_BASELINE.md).

## Dependency management

Dependabot is the default; do not add Renovate alongside it. Example for a
TypeScript repository (adapt the ecosystems to what the repository actually
contains; never ship a config for a manifest that does not exist):

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: npm            # or: pip, cargo, github-actions, bundler
    directory: "/"
    schedule:
      interval: weekly
      day: monday
      timezone: UTC
    open-pull-requests-limit: 5
    commit-message:
      prefix: "chore(deps)"
      include: scope
    groups:
      tooling:
        patterns: ["@types/*", "typescript", "vite"]
        update-types: ["minor", "patch"]

  - package-ecosystem: github-actions
    directory: "/"
    schedule:
      interval: weekly
```

- Security updates stay visible: no auto-merge, ever.
- Grouped updates keep low-risk tooling in one reviewable pull request.
- A repository with no manifest for an ecosystem gets no config for it.

## Issue and pull request hygiene

- One pull request, one purpose.
- Titles are searchable: what changed, not "update".
- The pull request template is short on purpose; fill it in, do not write an
  essay in it.
- Close stale branches. A branch older than a month with no pull request is
  either finished (merge or delete it) or abandoned (delete it).

## Repository ownership

- Every repository that matters has a `CODEOWNERS` file with real, verifiable
  owners (see [GOVERNANCE.md](GOVERNANCE.md)).
- Security-sensitive paths (`.github/`, `SECURITY.md`, workflow files,
  permission and authorization code) always have a named human owner.
- Ownership files are reviewed when people change roles, not when something
  breaks.

## When to split a repository

Split when the change cadence, the audience, or the blast radius differs, not
to make the folder tree look organized. A public documentation site and a
private runtime do not belong together; a config file and the service that
reads it do.

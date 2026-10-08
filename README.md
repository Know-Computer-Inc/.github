# Know-Computer-Inc/.github

The organization-level repository for **Know Computer, Inc.**: the public
organization profile, default community health files, issue and pull request
templates, workflow templates, and the engineering standards that apply across
Know repositories.

Everything here is policy, templates, and identity, no application code.

## What GitHub uses from this repository

| Path | Effect |
|---|---|
| `profile/README.md` | The public organization profile shown on the organization home page. **Requires this repository to be public.** |
| `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `SECURITY.md`, `SUPPORT.md`, `PULL_REQUEST_TEMPLATE.md` | Default community health files for Know repositories that do not define their own. A repository-local file always wins. |
| `.github/ISSUE_TEMPLATE/` | Default issue forms and issue configuration for repositories without their own. |
| `.github/workflows/` | CI for **this** repository (and reusable definitions, if any are added). |
| `workflow-templates/` | Starter workflows offered when creating a new workflow in a Know repository. |
| `.github/CODEOWNERS` | Review ownership for the files in this repository. |
| `.github/copilot-instructions.md` | Organization-level instructions for GitHub Copilot. |
| `.github/dependabot.yml` | Keeps this repository's own GitHub Actions pins current. |
| `docs/` | Organization-wide engineering standards. |

## Repository structure

```text
.
├── profile/
│   ├── README.md                 # public organization profile
│   └── assets/                   # brand assets derived from the official site design
├── .github/
│   ├── CODEOWNERS
│   ├── copilot-instructions.md
│   ├── dependabot.yml
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.yml
│   │   ├── feature_request.yml
│   │   ├── engineering_improvement.yml
│   │   ├── documentation.yml
│   │   └── config.yml
│   └── workflows/
│       └── ci.yml                # static validation of this repository
├── workflow-templates/
│   ├── python-ci.yml             # + .properties.json metadata
│   ├── node-ci.yml
│   ├── rust-ci.yml
│   └── dependency-audit.yml
├── docs/
│   ├── ENGINEERING_PRINCIPLES.md
│   ├── REPOSITORY_STANDARDS.md
│   ├── SECURITY_BASELINE.md
│   ├── AI_ENGINEERING_POLICY.md
│   ├── GOVERNANCE.md
│   ├── adr/                      # Architecture decision records: README + TEMPLATE
├── scripts/
│   └── validate_repo.py
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── SECURITY.md
├── SUPPORT.md
├── PULL_REQUEST_TEMPLATE.md
└── README.md
```

## Validation

Static validation runs in CI (`.github/workflows/ci.yml`) and locally:

```sh
python -m pip install pyyaml
python scripts/validate_repo.py
```

It checks that required files exist, that every YAML file parses, that issue
forms match GitHub's supported schema, that workflows declare least-privilege
permissions and pin actions to commit SHAs, that relative Markdown links
resolve, and that no credential-shaped strings are committed.

**Static validation is not proof of a control.** It does not demonstrate that a
workflow has run on GitHub, that branch protection is enabled, or that a
security feature is active. For the difference between recommended policy and
verified configuration, see [docs/SECURITY_BASELINE.md](docs/SECURITY_BASELINE.md).

## Standards in this repository

- [Engineering principles](docs/ENGINEERING_PRINCIPLES.md): how Know makes technical decisions.
- [Repository standards](docs/REPOSITORY_STANDARDS.md): READMEs, commands, tests, CI, dependencies.
- [Security baseline](docs/SECURITY_BASELINE.md): controls expected of Know repositories, plus what is actually configured today.
- [AI engineering policy](docs/AI_ENGINEERING_POLICY.md): what AI agents may and may not do in Know repositories.
- [Governance](docs/GOVERNANCE.md): who approves what, and how little process that requires.
- [ADR process](docs/adr/README.md): recording decisions worth keeping.

## Status of this repository

- The organization profile in `profile/README.md` is written to be publishable
  as-is, but **this repository is private**, and the organization profile will
  not render until GitHub's public `.github` repository requirement is met.
- Security and conduct reports reach m@know.computer (Mattia Ciuni, CEO at
  Know Computer); private vulnerability reporting is preferred where enabled.

Changing visibility, branch protection, organization settings, or permissions
requires explicit human approval, see [docs/GOVERNANCE.md](docs/GOVERNANCE.md).

## License

No license has been declared for this repository yet. That is a deliberate
pre-publication decision, not an oversight: choose and add a `LICENSE` before
publishing.

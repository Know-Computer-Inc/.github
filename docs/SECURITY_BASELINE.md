# Security Baseline

The standard every Know repository is expected to meet, and an honest record of
what is actually configured today.

## How to read this document

Two things are deliberately separated:

- **Recommended policy:** what we intend every repository to have. Written
  here, agreed as intent, *not* proof that it is active.
- **Verified configuration:** what was observed directly through the GitHub API
  on the date stated. Everything here was checked, not assumed.

**Nothing is protected because this document says it should be.** Controls only
exist when they are configured in GitHub and confirmed afterwards.

## Verified configuration

Observed via the GitHub API on **2026-10-08**, authenticated as an organization
administrator. This is a point-in-time audit, not continuous monitoring.

| Control | Observed state |
|---|---|
| Repositories | 7, all **private**; 0 public |
| Organization teams | **Three teams as of 2026-10-08:** `Engineering` (private, @mattiaciuni as maintainer), `Contributors` (visible, read baseline), `Reviewers` (visible, write baseline). CODEOWNERS still uses a named human. |
| Branch protection on default branches | **Not enabled** on any sampled repository (all report `protected: false`) |
| Branch protection on `.github` | **Enabled 2026-10-08** on `main`: required status check `Repository validation`, no force-push, no deletions, administrators included |
| Required pull request reviews | Not observed as enforced anywhere |
| Secret scanning / push protection | **Enabled on `.github`** (public). Private repositories returned 422: plan-limited (requires GitHub Advanced Security) |
| Dependabot alerts | **Enabled on all 7 repositories** (2026-10-08) |
| Private vulnerability reporting | Not enabled; the endpoint returned 404 on this plan |
| CODEOWNERS | Present in one public-facing repository (`@mattiaciuni`); absent from `.github` at audit time |
| CI | Present in four repositories, each with `permissions: contents: read` |
| Dependabot updates | Configured in one repository (npm + github-actions, weekly, no auto-merge) |

Some features (secret scanning and push protection on private repositories,
private vulnerability reporting) are plan-limited on GitHub and may not be
available until the organization's plan changes. That is a business decision,
not an oversight.

## Recommended policy

### 1. Repository access and visibility

- Access follows least privilege: write access to people who actually commit,
  read access to people who actually need the code.
- Visibility changes (private → public) are an explicit business decision, made
  repository by repository, after a content review (see
  [publication checklist](#publication-checklist)).
- Outside collaborators are added per repository, never organization-wide,
  and only with a stated reason and an end date.
- No shared accounts. Automation uses its own identity.

### 2. Branch protection and review

For the default branch of every repository that receives contributions:

- Pull requests required for direct pushes; no force-push; no branch deletion.
- At least one approving review from a person with write access.
- Dismiss stale approvals when new commits are pushed.
- Require the branch to be up to date before merge once CI is stable.
- Require all conversation threads to be resolved.
- Require status checks to pass (the repository's own CI).
- `CODEOWNERS` review required for security-sensitive paths.
- Include administrators, so protection applies to everyone, including
  humans who would rather bypass it and agents that cannot.

Small pre-seed trade-off: on a team of one or two people, one required review
from a second person may not always be possible. If that is the reality,
document the exception in the repository rather than quietly disabling
protection for everyone.

### 3. Secrets and credentials

- No secret, key, token, or `.env` file is ever committed, not even for a
  test. Use obviously fake values in fixtures.
- Credentials live in GitHub Actions secrets, environment secrets, or a
  password manager, and are scoped to one environment.
- Every secret has an owner and a rotation interval (90 days is a reasonable
  default; immediate on any suspected exposure).
- Fork-facing workflows never receive secrets: no `pull_request_target` unless
  a reviewed use case exists, and never with `secrets.*` passed to untrusted
  checkout code.
- Leaked credentials are rotated *first*, investigated second.

### 4. Dependency security

- Dependabot security updates enabled for every repository with a supported
  manifest; version updates weekly, grouped for low-risk tooling.
- No automatic merging of dependency updates. Every dependency pull request
  passes CI and human review.
- New dependencies require justification in the pull request: purpose,
  alternatives, maintenance status, license.
- Known-vulnerability audits run in CI (`npm audit`, `pip-audit`,
  `cargo audit`, whichever matches the stack).
- Prefer minimal dependency surface: the standard library is the safest
  dependency.

### 5. Supply-chain security and GitHub Actions

- Third-party actions are pinned to a **full commit SHA**, with the intended
  version in a trailing comment:
  `uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1`
- Only actions from the `actions/` and `github/` orgs, or tools the team has
  deliberately evaluated, are used.
- Pins are updated through Dependabot (`github-actions` ecosystem) or a
  scheduled review, never by copying a tag from a blog post.
- Workflow changes are reviewed like code: they can exfiltrate secrets.
- Generated artifacts (bundles, images) are built by CI, not by hand, and are
  traceable to a commit.

### 6. CI isolation and permissions

- Every workflow declares top-level `permissions: contents: read` (or the
  minimum the job needs). Permissions are granted per job, not per repository.
- Workflows triggered by untrusted input (fork pull requests) get no secrets
  and no write token.
- No workflow deploys to production automatically on merge. Deployment is a
  separate, deliberate workflow, gated by environment protection rules.
- No workflow merges pull requests automatically.
- `pull_request_target` is avoided by default; a use case must be written down
  before it is introduced.

### 7. Production deployment authority

- Only named humans hold deployment credentials.
- Production deployment happens from a protected branch, through a reviewed
  workflow, with the commit that was reviewed.
- Agents never hold production deployment authority.
- Rollback is rehearsed: every deployable repository documents how to return
  to the previous known-good commit.

### 8. Incident response

1. **Contain.** Revoke or rotate the affected credential, disable the affected
   path, stop the automation if it is acting.
2. **Assess.** What was accessed, by whom, when, and what else shares the
   compromised credential.
3. **Report.** Affected users and, where relevant, follow
   [SECURITY.md](../SECURITY.md) disclosure expectations.
4. **Fix and learn.** Patch the root cause, then write down what allowed it.
   The post-mortem has no blame and no exceptions.

Incident records live in a private location; the *lessons* that can be shared
become changes to this document.

### 9. Auditability

- Every change to a repository goes through a pull request or a reviewed
  commit; no unattributed edits to protected branches.
- Automation commits under an identity that identifies it as automation.
- Agent and CI actions must be attributable to a repository, a commit, and an
  authorization decision after the fact.
- Retain CI run history and review history; they are the evidence trail.

## Checklist for repository owners

Copy this into the repository's own security notes and fill in the status
honestly. A checked box without an observation is a false statement.

| # | Control | Status |
|---|---|---|
| 1 | Private vulnerability reporting enabled (Settings → Code security) | ☐ |
| 2 | Branch protection on default branch: PR required, 1 review, no force-push | ☐ |
| 3 | Required status checks listed and actually passing | ☐ |
| 4 | `CODEOWNERS` present with real, verifiable owners | ☐ |
| 5 | Dependabot security updates enabled | ☐ |
| 6 | Dependabot version updates configured for the real ecosystems in this repo | ☐ |
| 7 | All workflow `uses:` pinned to commit SHAs | ☐ |
| 8 | Workflows declare least-privilege `permissions` | ☐ |
| 9 | No secrets committed; `.env`-style files ignored | ☐ |
| 10 | Dependency audit job running in CI | ☐ |
| 11 | Secret scanning / push protection enabled or explicitly waived for plan reasons | ☐ |
| 12 | Deployment gated on a protected environment with human approvers | ☐ |
| 13 | `SECURITY.md` present and its reporting route verified to work | ☐ |
| 14 | Repository README documents how to build, test, and report problems | ☐ |

## Publication checklist

Before a private repository becomes public:

1. Read every tracked file for internal architecture, credentials, customer or
   partner references, and business plans.
2. Check the full Git history (`git log -p --all`), not just the current tree.
3. Verify every external link in the repository resolves.
4. Confirm security and conduct reporting routes actually reach a human.
5. Confirm licenses and third-party attributions are correct.
6. Remove or relocate internal-only documents (inventory, operational runbooks).
7. Record who approved the visibility change.

## What requires explicit approval

Enabling any control above that changes organization settings (branch
protection, security features, visibility, member roles, workflow permissions)
requires explicit human approval. See [GOVERNANCE.md](GOVERNANCE.md) for who
approves what. This document recommends; it does not authorize.

# Repository Inventory

**INTERNAL — do not publish.** This document names private Know repositories and
records their state. It must be removed from this repository, or moved to a
private governance location, before `.github` is made public. See
[SECURITY_BASELINE.md](../SECURITY_BASELINE.md) → *Publication checklist*.

Audit date: **2026-10-08**. Source: GitHub API, authenticated as an organization
administrator. Everything below was observed; nothing is inferred from a
repository name.

## Inventory

| Repository | Visibility | Default branch | Primary language | CI workflows | Community files | License |
|---|---|---|---|---|---|---|
| `Know` | private | `main` | Python (with Rust crates and TypeScript packages in-tree) | none | `README.md`, `LEGGIMI.md` | none detected |
| `Know-Website` | private | `main` | JavaScript / TypeScript | `ci`, `deploy-staging`, `deploy-production` | `README.md`, `PULL_REQUEST_TEMPLATE.md`, `CODEOWNERS`, `dependabot.yml` | none detected |
| `Know-Docs` | private | `main` | — (empty repository) | none | none | none |
| `Know-Teams-Agents` | private | `main` | JavaScript | `validate` | `README.md`, `CONTRIBUTING.md`, `SECURITY.md`, `AGENTS.md`, `LICENSE-NOTICE.md` | non-standard (`NOASSERTION`) |
| `Know-Team-MCP` | private | `main` | TypeScript | `ci`, `security` | `README.md`, `CONTRIBUTING.md`, `SECURITY.md`, `AGENTS.md`, `LICENSE-NOTICE.md` | non-standard (`NOASSERTION`) |
| `Know-Agent-Runtime` | private | `ai/bootstrap-runtime` | Python | `ci`, `security` | `README.md`, `CONTRIBUTING.md`, `SECURITY.md`, `AGENTS.md`, `LICENSE-NOTICE.md` | non-standard (`NOASSERTION`) |
| `.github` | private | `main` | — (empty at audit time) | none | none | none |

## Observations worth acting on

- **No branch protection anywhere** was observed on sampled default branches.
  Highest-value setting change available, once approved.
- **No GitHub teams exist**, so `CODEOWNERS` cannot use team slugs yet. Use
  named accounts (`@mattiaciuni`, verified as organization administrator with
  admin rights on `.github`) until teams are created.
- **`Know-Agent-Runtime` defaults to `ai/bootstrap-runtime`**, not `main`. That
  branch name reads like work-in-progress but is the default branch, so it is
  what clones, CI triggers, and protection rules target. Either rename it to
  `main` or document the choice.
- **`Know-Docs` is empty** (the Git tree endpoint returns `409 Conflict`). The
  documentation repository has no content yet; do not link to it publicly.
- **Three repositories carry a `LICENSE-NOTICE.md`** that GitHub cannot
  classify. The intended license for each repository is undecided; this needs a
  decision before any repository goes public.
- **`Know-Website` already sets a good example**: CODEOWNERS, PR template,
  Dependabot (npm + github-actions, weekly, grouped, no auto-merge), CI with
  least-privilege `permissions`, and dedicated audit scripts.
- **The declared production domain does not resolve.** The website repository
  states `useknow.computer` as the canonical domain; DNS lookup on 2026-10-08
  returned NXDOMAIN, and the repository README states deployment is prepared but
  not activated. Do not publish or link that domain until it serves content.

## Conventions observed

- CI workflows declare top-level `permissions: contents: read` and use
  concurrency cancellation; action references are tag-pinned (`@v7`), not
  SHA-pinned.
- Dependency updates are handled with Dependabot where configured, explicitly
  without auto-merge.
- Commit and pull request titles follow Conventional Commit-style prefixes
  (`chore(deps)`, `feat/fix`), at least in `Know-Website`.
- Several internal repositories publish their own `AGENTS.md` as the entry point
  for AI contributors, with rules that match this organization's
  [AI Engineering Policy](../AI_ENGINEERING_POLICY.md).

## Visibility recommendations

Recommendations only. No visibility was changed by this audit.

| Repository | Recommended eventual visibility | Rationale |
|---|---|---|
| `.github` | **Public** | Required for the organization profile to render; must pass the publication checklist first. |
| `Know-Website` | **Public** (business decision) | Marketing site code is normally public; review for roadmap and infrastructure detail first. |
| `Know-Docs` | **Public** when it has content | Documentation has no value private; nothing exists yet. |
| `Know` | **Decision required** | Contains product IP and the shape of the product. Decide deliberately — public source, public read-only subset, or stay private. |
| `Know-Teams-Agents` | **Private** | Canonical agent identities, roles, and internal company context. |
| `Know-Team-MCP` | **Private** | Internal capability boundary and permission configuration. |
| `Know-Agent-Runtime` | **Private** | Orchestration, approvals, and authorization for autonomous systems. |

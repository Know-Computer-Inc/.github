# Governance

Who decides what at Know, and how little process that actually requires.

Know is a pre-seed company. The point of this document is not bureaucracy; it
is to make sure that the decisions which are hard to undo are made deliberately,
by a person who understood they were making them, and are recorded somewhere
they can be found later.

Everything here is **recommended policy**. Actual GitHub roles, branch
protection, and organization settings are configured separately and verified
afterwards; see [SECURITY_BASELINE.md](SECURITY_BASELINE.md) for what has been
observed. Nothing in this file grants permissions.

## Roles

| Role | Responsibility |
|---|---|
| **Repository maintainer** | Owns a repository's direction, merges pull requests, keeps its README, tests, and CI honest. |
| **Code reviewer** | Evaluates correctness, clarity, tests, and scope. Responsible for what they approve. |
| **Security reviewer** | Reviews changes touching authorization, secrets, data access, agent boundaries, and workflows. A role, not necessarily a separate person; at current team size the same human may hold both. |
| **Organization administrator** | Manages members, teams, repository settings, and security features. The only role that changes organization configuration. |
| **Release owner** | Authorizes publication: releases, tags, public visibility changes, production deployments. |
| **AI automation identity** | May open pull requests and push branches when authorized. Holds no approval, merge, deployment, or configuration authority, by construction, not by agreement. |

One person may hold several roles. The roles must still be *named*, so it is
clear who to ask and who was accountable when something goes wrong.

## Approval expectations

| Decision | Approves |
|---|---|
| Merging to a protected default branch | One code reviewer with write access (two for security-sensitive paths) |
| Making a repository public | Organization administrator + release owner, after the publication checklist |
| Changing `SECURITY.md`, `CODE_OF_CONDUCT.md`, this document, or `AI_ENGINEERING_POLICY.md` | Organization administrator, with explicit human review, never by an agent acting alone |
| Changing branch protection, repository settings, or organization settings | Organization administrator |
| Granting, changing, or revoking repository access | Organization administrator |
| Adding or changing a secret or credential | Named owner of that credential, recorded where the team can see that it exists |
| Changing a workflow's permissions or triggers | Code reviewer + security reviewer (may be the same person) |
| Production deployment | Release owner or explicitly delegated human, from a protected branch |
| New third-party integration or service | Organization administrator, with the data it will touch written down |
| Default branch rename or deletion | Organization administrator, announced to everyone with open pull requests |
| Repository deletion | Organization administrator + release owner |
| Expanding an AI agent's authority | Human owner of that authority, in writing, with scope and expiry |

## Principles that keep this light

- **Approvals are for irreversible or broad-blast-radius decisions.** If a
  mistake is cheap to revert, do not gate it, revert it.
- **The person doing the work does not approve their own high-risk change**
  when another person is available. When no other person is available, the
  exception is written into the pull request instead of being hidden.
- **Agents never approve, merge, or authorize their own work.** This is
  enforced by permissions (an agent identity cannot be granted review
  authority on its own changes), not by instruction files.
- **Say no out loud.** A declined request gets a reason in writing; a silently
  ignored request is a process failure.
- **Revisit when it hurts.** If a rule costs more than the risk it controls,
  change the rule deliberately, do not erode it quietly.

## Escalation

1. Unclear authority → stop, ask the repository maintainer.
2. Maintainer unavailable and the decision blocks work → organization
   administrator.
3. Security incident → follow the incident response in
   [SECURITY_BASELINE.md](SECURITY_BASELINE.md); containment does not wait for
   approval.
4. Disagreement about direction → write both positions in an issue or an ADR,
   then decide. Consensus is a goal, not a requirement.

## Review authority

- Review authority comes from GitHub permissions on a specific repository, and
   is granted by an organization administrator to a named human.
- It is never inherited from an AI tool's suggestion, an agent's role
   definition, or a policy file in this repository.
- Reviewers are responsible for what they approve. Rubber-stamping a
   security-sensitive change transfers the responsibility, not the risk.
- CODEOWNERS files list real accounts only. If a team does not exist on
  GitHub, its name does not appear in CODEOWNERS; see
  [SECURITY_BASELINE.md](SECURITY_BASELINE.md) §2.

## Records

Decisions worth finding twice are written down:

- **Architecture and long-term technical decisions** → [adr/](adr/README.md)
- **Security decisions and control status** → [SECURITY_BASELINE.md](SECURITY_BASELINE.md)
- **Process changes** → the relevant document in this repository, in a pull
  request, so the change is visible and reviewable
- **Incidents** → private incident records; shareable lessons come back into
  these documents

If a decision exists only in someone's memory, it is a risk, not a decision.

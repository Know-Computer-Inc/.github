# Contributing

Know Computer builds in public where it makes sense and in private where it
does not. This document describes the default expectations for anyone changing
a Know repository.

## Which repositories accept contributions

- **Public repositories** accept contributions through issues and pull
  requests, following this document plus any repository-local
  `CONTRIBUTING.md`.
- **Private repositories** do not accept external contributions. Their
  maintainers work internally; opening an issue or pull request there will not
  be possible or useful.

A repository-local `CONTRIBUTING.md` always wins over this document. If a
repository documents a different command, a different review rule, or a
different merge strategy, follow the repository.

## Before you start

1. Read the repository `README.md`: how to set it up, how to run it, how to
   test it.
2. Read [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) and [SECURITY.md](SECURITY.md).
3. For anything non-trivial, open an issue first. A short conversation before
   code saves both sides from writing the wrong thing.
4. Search existing issues and pull requests to avoid duplicating work.

## Reporting bugs

Use the **Bug report** issue form in the affected repository. The form asks for
reproduction steps, expected and actual behaviour, and environment details — a
bug we cannot reproduce is a bug we cannot fix.

- Reproduce it on the current default branch before reporting.
- Strip credentials, tokens, personal data, and internal paths from logs and
  screenshots.
- If the bug is security-sensitive, stop and follow [SECURITY.md](SECURITY.md)
  instead.

## Proposing changes

```sh
git clone <the repository>
git checkout -b <type>/<short-description>
# make the change
git push -u origin <type>/<short-description>
# open a pull request against the default branch
```

Branch names are free-form; the pull request is not. Every pull request must
state, in its first paragraph, what the change does and why it is needed.

### What we look for

- **Small, reviewable diffs.** Split work that mixes an unrelated refactor with
  a behaviour change.
- **Evidence, not assertion.** Say which commands you ran and what they
  printed. "Tested locally" without the command means nothing.
- **Tests that fail before your change and pass after it** — for bug fixes —
  or tests that cover new behaviour — for features.
- **No drive-by reformatting.** Whitespace and style changes belong in their
  own commit or pull request.
- **Documentation updated with the code.** If a change alters setup steps,
  commands, configuration, or public behaviour, update the README or the
  relevant document in the same pull request.

### Coding quality

- Match the language, structure, and naming already used in the repository.
  Consistency with the surrounding code beats personal preference.
- Keep functions small enough to read and name them so the name is true.
- Do not add a dependency when the standard library or an existing dependency
  already solves the problem. New dependencies need a justification in the pull
  request: what it does, why the alternatives lose, who maintains it.
- Avoid speculative abstraction. Two examples make a pattern; one does not.
- Comments explain *why*, not *what*. Code that needs narration to be
  understood should usually be restructured instead.

### Testing

- Run the repository's own test command before opening the pull request, and
  paste the exact command and result into the pull request.
- A change without tests is acceptable only when the repository has no test
  harness and the change is documentation-only or trivially verifiable; say so
  explicitly.
- Do not weaken, skip, or delete an existing test to make a change pass. Fix the
  test only if the test itself is wrong, and explain why in the pull request.
- Never claim a test passed unless it actually ran and passed.

### Compatibility

- Keep changes backward compatible with existing data, configuration, and
  saved state unless the pull request says otherwise and explains the
  migration.
- Prefer additive changes over breaking ones. If a breaking change is
  unavoidable, it needs explicit maintainer approval and a migration note.

## Security-sensitive contributions

Changes that touch authorization, data access, secret handling, cryptography,
sandboxing, or agent permissions are reviewed more strictly than ordinary
changes.

- Call the sensitivity out in the pull request description.
- Explain what could go wrong if the change is subtly wrong.
- Expect a human security-minded reviewer, and expect the review to take
  longer.
- Do not include real credentials, tokens, or personal data in tests or
  fixtures. Use obviously fake values.

## Review

- A pull request is ready for review when it is complete, tested, and the
  description is written — not when the author wants feedback.
- Reviewers evaluate correctness, clarity, tests, security impact, and scope.
  Expect pushback on all five.
- Review is a discussion, not a verdict negotiation: either side can propose a
  different implementation, but a maintainer decides.
- Reviews are expected to be substantive; "LGTM" without reading the diff does
  not satisfy a required-review rule.
- Security-sensitive files (security policy, permissions, workflow definitions,
  review-ownership configuration) require explicit human review. See
  [docs/AI_ENGINEERING_POLICY.md](docs/AI_ENGINEERING_POLICY.md).

### AI-assisted contributions

Contributions drafted or substantially written by an AI agent are welcome where
the repository accepts contributions, under two conditions:

1. The author has read, tested, and can defend the change as if they wrote it
   themselves.
2. The pull request states that AI assistance was used, at what level (suggestion,
   draft, agent-prepared), and who reviewed the result.

AI-generated code is reviewed as code. It does not inherit trust, and an agent
never approves, merges, or otherwise authorizes its own work.

## Merging

- Maintainers merge; authors do not merge their own pull requests.
- The default merge strategy is whatever the repository has configured. Where a
  repository has no preference, squash merging is a reasonable default for
  small, self-contained changes.
- A pull request that does not pass its continuous integration checks is not
  merged, except by an explicit maintainer decision recorded in the pull
  request.
- Production deployment is a separate, deliberate action. Merging is not
  deploying.

## Dependency changes

- Pin and upgrade deliberately; do not upgrade a dependency "while we are here".
- Security updates are prioritized and should not be bundled with feature work.
- Include the reason, the version delta, and the result of the project's audit
  command in the pull request.
- One pull request per dependency group; avoid mega-updates that cannot be
  reviewed.

## Licensing and provenance

- Only contribute code you have the right to contribute.
- Do not paste code from Stack Overflow, GitHub, or anywhere else without
  checking its license and, where required, attributing it.
- Keep generated content identifiable: if a tool produced a file, say so.

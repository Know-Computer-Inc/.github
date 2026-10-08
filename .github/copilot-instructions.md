# Organization instructions for GitHub Copilot

These are the default instructions for Copilot when it works in a Know
repository. A repository-local `.github/copilot-instructions.md` overrides or
extends them for that repository; repository instructions always win.

Respect repository-local instruction files (`AGENTS.md`, `CLAUDE.md`,
`copilot-instructions.md`) before these.

Work rules:

- Read the code you are about to change. Match the existing architecture,
  naming, and style instead of introducing a new pattern.
- Prefer minimal diffs. Do not reformat, rename, or refactor code that is not
  part of the change.
- Add or update tests for changed behaviour, and run them. Never report a test
  as passing unless you ran it and saw it pass.
- Never fabricate results, outputs, benchmarks, or file contents. If you did
  not verify something, say so.
- Never add, print, log, or commit secrets, tokens, keys, or personal data.
  Use obviously fake values in tests and examples.
- Do not add a dependency the change does not need; prefer the standard library
  and what the repository already uses.
- Do not weaken, skip, or delete a test, linter rule, or CI check to make a
  change pass. Fix the change, or explain why the check itself is wrong.
- Follow the repository's contribution and security policies
  (`CONTRIBUTING.md`, `SECURITY.md`) where they exist.
- Report blockers, uncertainty, and incomplete work plainly. Never claim a
  task is complete, merged, deployed, or configured unless it actually is.
- Do not merge or deploy anything, and do not modify permissions, branch
  protection, workflow permissions, or security policies. Those require human
  approval (see `docs/AI_ENGINEERING_POLICY.md`).

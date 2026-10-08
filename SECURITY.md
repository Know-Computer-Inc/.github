# Security Policy

A vulnerability in Know software is not just a bug — it can change what an
autonomous system is allowed to read, write, or execute on someone's computer.
We treat security reports accordingly.

## Supported versions

Know does not publish versioned releases for most repositories today.

- Only the **tip of the default branch** of each repository is maintained.
- Older commits, branches, and any archived repositories are unsupported.
- If a deployed service ever exists, its supported version will be documented
  here at that time.

## Reporting a vulnerability

**Report privately. Do not open a public issue, do not describe the issue in a
pull request or commit message, and do not discuss it in public channels.**

Use, in order of preference:

1. **GitHub private vulnerability reporting**, if it is enabled on the
   repository where you found the issue: *Security* → *Report a vulnerability*
   on that repository.
2. Otherwise, contact a Know organization administrator directly through GitHub
   and state that you are reporting a security vulnerability. Ask for a private
   channel and wait for one before sharing details.

<!--
  PUBLICATION BLOCKER (must be resolved before this repository is made public):
  private vulnerability reporting has not been verified as enabled for this
  organization (see docs/SECURITY_BASELINE.md, checklist item 1). Either enable
  it on the repositories that will be public, or publish a verified monitored
  security address as a third route above. Do not publish an invented address.
-->

A useful report contains:

- what you found and where (file, function, configuration key, endpoint);
- a concrete reproduction: a failing test, a sequence of commands, or minimal
  proof-of-concept code;
- the impact you believe it has — specifically, whether it lets a component read
  or modify data or act beyond the authority it was granted;
- whether you have already triggered it against any real system or data;
- any suggested remediation, if you have one.

## What we ask of you

- **Give us time to fix the issue before disclosing it.** We will work with you
  on a coordinated disclosure timeline. We do not publish a fixed response or
  fix deadline; realistic timelines depend on severity and reproduction quality,
  and we will be honest with you about where a report stands.
- **Do not exploit the issue** beyond what is needed to demonstrate it: no
  exfiltration of real user data, no destructive actions, no access to systems
  or accounts that are not yours.
- **Do not include secrets, keys, credentials, or personal data** in the report
  beyond what is strictly necessary to demonstrate the problem.
- **Do not impersonate or harass** anyone while researching.

## What we will do

- Acknowledge the report when a human has read it.
- Assess severity and reproduction, and keep you updated while we investigate.
- Fix the issue and credit you if you want credit (many do not).
- Tell you honestly if we cannot reproduce it, or if we consider it out of
  scope.

There is **no bug bounty, no reward programme, and no public credit
requirement**. Reports are handled by the maintainers. Reports from automated
scanners that contain no reproduction or specific impact will not be actioned.

## Sensitive information handling

- Security details shared with us stay within the small set of people who need
  them to fix the issue.
- Do not put vulnerability details into any file, log, ticket, or transcript that
  is not already part of a private, access-controlled channel.
- If a credential or secret is disclosed accidentally, treat it as compromised
  immediately: rotate it, then report the exposure.

## Public channels are for public problems

Feature questions, bug reports without security impact, and documentation
problems belong in the normal issue templates of the repository they affect.
Anything that describes a way to bypass authorization, read data a user did not
consent to, or execute commands unexpectedly belongs here instead.

See also: [SUPPORT.md](SUPPORT.md) for where to ask for help, and
[docs/SECURITY_BASELINE.md](docs/SECURITY_BASELINE.md) for the security
standards Know repositories are expected to meet.

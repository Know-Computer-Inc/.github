# Architecture Decision Records

Short, dated records of decisions we expect to still matter in a year.

## When to write one

Write an ADR when a decision:

- is expensive to reverse (data model, storage, protocol, public interface);
- affects security, authorization, privacy, or the trust boundary;
- settles an argument that would otherwise be re-had every quarter;
- chooses between designs with genuinely different operational consequences.

Do **not** write one for routine changes: naming, file layout, minor refactors,
tool upgrades within the same stack. If you are unsure, prefer a good pull
request description; a thin ADR is worse than none.

## How to use this folder

1. Copy [TEMPLATE.md](TEMPLATE.md) to `NNNN-short-kebab-title.md`.
2. Number decisions sequentially; never renumber or reuse a number.
3. Fill in every section. "None" and "not applicable" are acceptable answers;
   blanks are not.
4. Open it as a pull request so the decision gets read while it is fresh.
5. Status moves forward only: `Proposed` → `Accepted` → `Superseded by NNNN`.
   Decisions are not deleted; superseded ones stay for context.

## Index

| ADR | Title | Status |
|---|---|---|
| — | No decisions recorded yet. | — |

Add a row here when you add a decision. This repository deliberately ships no
fabricated history: the first ADR is the first real decision.

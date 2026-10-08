# Engineering Principles

These are the principles Know engineers use to make decisions when the answer is
not obvious. They are written to be argued with: each one exists because the
opposite failure is easy to imagine in our own systems.

## 1. Evidence over confidence

A system is only as reliable as what has been demonstrated for it. Say which
command you ran, what it printed, and on which commit. A green check is worth
more than a strong opinion; an honest "not tested yet" is worth more than a
claim. Confidence without evidence is noise, no matter who is speaking,
including us, including our models.

## 2. Simplicity is a feature

Every layer, dependency, service, and abstraction is a liability that accrues
interest in maintenance, debugging, and security review. Complexity must earn
its place by removing more friction than it creates. When two designs solve the
problem, prefer the one with fewer moving parts, and prefer deleting the
problem altogether to building something clever around it.

## 3. Security is architecture

Authorization, isolation, and boundaries are design decisions, made in the
first sketch of a system, not a checklist applied after it works. A control
bolted on at the end is a claim; a control built into the structure is a
property. If a design cannot state clearly who may do what to which data, the
design is not finished.

## 4. Human authority is explicit

Autonomy is not permission. What an automated system may do is written down,
scoped to a task, limited in time, and revocable by a person. Silence is never
consent, absence of a rule is never a grant, and no component (human or
machine) gets to expand its own authority. Anything that can act must be
auditable after the fact.

## 5. Reliability before scale

Prove the core loop behaves correctly, fails safely, and can be recovered
before optimizing for growth that has not arrived. Premature scale is the most
expensive way to feel productive. Correctness, observability, and recovery come
first; throughput is an optimization you can schedule.

## 6. Own the entire lifecycle

A change is not done when it runs. It is done when it is tested, its failure
modes are understood, its behaviour is observable, its recovery path exists,
and someone is accountable for maintaining it. "Somebody else's problem" is a
design smell, not an organizational boundary.

## 7. Make the computer more useful

Engineering is not an end in itself. The work exists to extend what a person
can understand, retrieve, decide, and do, with less friction than they have
today. If a system requires people to manage more software, more configuration,
and more explanations, the engineering has failed regardless of how elegant it
is underneath.

## 8. Build for the long term

Choose the boring thing that still works in three years over the clever thing
that demos well this week. Maintainability is a feature users never see and
always feel. Optimize for the person who will read this code cold, in a hurry,
with incomplete context: that person is usually us.

---

## When principles conflict

Principles are inputs to judgment, not rules that override each other.

- **Evidence beats confidence, always.** If a principle is being used to defend
  an untested claim, it has been misapplied.
- **Security and human authority outrank convenience.** A faster path that
  weakens a boundary is not a faster path.
- **Reliability outranks scale, and simplicity outranks feature count.** When
  scope is contested, ship less and prove it.
- **Write down the tie-breaker you used.** The decision record outlives the
  argument. See [adr/](adr/README.md) for decisions worth keeping.

A principle that never costs anything is decoration. If following one of these
has ever slowed a release down, it is working.

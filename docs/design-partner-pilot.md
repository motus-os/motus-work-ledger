# Controlled Design-Partner Pilot

> Status: draft alpha
> Scope: one external workflow, one reconstruction test, no broad adoption claim

This packet defines the first external Motus Work Ledger pilot. It is deliberately
narrow. The pilot tests whether Motus-compatible Work Receipts help a real team
reconstruct consequential work better than pull requests, CI logs, tickets, chat,
and memory alone.

## Pilot Thesis

Motus Work Ledger is useful if a reviewer can inspect a Work Receipt and answer:

1. What work was attempted?
2. Who or what performed it?
3. What evidence existed?
4. What outcome was claimed?
5. What was accepted, rejected, pending, or not required?
6. What should happen next?

The pilot is not a claim that Motus is organization-ready, a standard, a
compliance product, or a workflow system.

## Participant Scope

Use one external participant:

- one team or repository,
- one AI-assisted, CI, automation, or mixed human/tool workflow,
- one project cycle or 30 calendar days,
- one named pilot owner,
- one named reviewer for the reconstruction exercise.

Do not broaden the pilot to multiple teams, generic productivity measurement,
or organization-wide governance.

## Workflow Scope

The workflow should involve consequential work where reconstruction matters.

Good pilot candidates:

- AI-assisted code changes with CI validation,
- release-prep commands that produce artifacts,
- security or quality checks whose evidence should be retained,
- tool-driven triage followed by human acceptance,
- human plus agent handoff on a bounded task.

Poor pilot candidates:

- casual chat,
- all developer activity,
- keystroke or screen monitoring,
- generic time tracking,
- workflows where existing logs already answer the reconstruction questions well.

## Implementation Path

For the first pilot, prefer the lowest-friction path:

1. Use the released `motus-work-ledger` schemas, examples, validator, and
   receipt-only implementation as the canonical framework source.
2. Use `/motus` or another adapter only as an emitter when it reduces setup
   friction.
3. Validate every emitted Work Receipt with the conformance validator.
4. Keep raw logs, transcripts, and sensitive artifacts outside the receipt
   unless the participant explicitly chooses otherwise.
5. Never embed secrets in a receipt. Reference redacted evidence or digests
   instead.

If the participant implements directly from semantic conventions, they must use
`semconv/schema-map.md` and pass conformance before pilot data is counted.

## Artifacts

Every counted pilot run should produce:

- one Work Receipt JSON file,
- validator output,
- evidence references or artifact references,
- enough context for a reviewer to locate the original PR, CI run, ticket, or
  tool execution,
- a short operator note capturing setup friction and confusing fields.

Do not require raw transcript capture, screen recording, keystroke capture, or
employee activity streams.

## Privacy And Security Boundaries

Motus records consequential work facts, not worker activity streams.

Pilot defaults:

- prefer evidence references over embedded sensitive content,
- hash evidence when content cannot be shared,
- redact secrets and private customer data,
- never embed secrets in receipts, examples, logs, or pilot closeout notes,
- do not capture raw prompts or transcripts by default,
- do not record unrelated personal productivity data,
- document how to remove generated pilot artifacts.

If a participant needs confidential evidence, record a digest and a safe
reference rather than embedding the content.

## Success Metrics

Use both quantitative and qualitative evidence.

Minimum quantitative metrics:

- at least 20 validated Work Receipts, or all eligible runs if fewer than 20
  occurred during the agreed project cycle,
- zero receipts that require private Motus team knowledge to validate,
- one reconstruction exercise completed by a reviewer who did not perform the
  work.

Reconstruction metric:

- reviewer answers the six pilot thesis questions from the Work Receipt and
  referenced artifacts in under 5 minutes for a representative run.

Friction metric:

- setup and validation steps are clear enough that the participant can repeat
  them without live Motus-team assistance after initial onboarding.

Qualitative metric:

- participant states whether they would keep Work Receipts for this workflow,
  and why.

## Failure Criteria

The pilot fails or must be redesigned if any of these occur:

- receipts are not consulted during the reconstruction exercise,
- existing PR, CI, ticket, and chat artifacts are enough and the receipt adds no
  meaningful clarity,
- setup friction outweighs reconstruction value,
- receipts expose sensitive content unexpectedly,
- receipts cannot be validated without private knowledge,
- implementers following public docs produce schema-invalid receipts,
- the participant interprets Motus as surveillance, workflow control, or a
  compliance guarantee.

Failure is useful signal. Do not reinterpret failure as adoption success.

## Reconstruction Exercise

Select one real run after receipts exist.

Reviewer task:

1. Start from the Work Receipt.
2. Inspect only the receipt and referenced artifacts.
3. Answer the six pilot thesis questions.
4. Record time spent and any missing context.
5. Compare against the normal reconstruction path using PR, CI, ticket, chat,
   and memory.

The reviewer should not be the person who performed the work.

## Pilot Closeout

The closeout must include:

- participant and workflow description,
- dates covered,
- number of eligible runs,
- number of valid receipts,
- number of invalid receipts and why,
- reconstruction exercise result,
- setup friction notes,
- privacy or security issues,
- participant keep/stop decision,
- Motus changes required before the next pilot.

Use restrained language:

- "controlled design-partner pilot"
- "framework alpha"
- "Motus-compatible Work Receipts"

Avoid:

- "standard"
- "organization-ready"
- "compliance solution"
- "agent governance platform"
- "work control plane"

## Stop And Remove

A participant must be able to stop the pilot without changing their workflow
tooling.

Minimum stop path:

1. stop generating new Work Receipts,
2. retain or delete pilot receipts according to participant policy,
3. remove any adapter hook or CI step,
4. keep this repo and `/motus` optional.

The pilot must not make Motus a dependency for the participant's normal
workflow execution.

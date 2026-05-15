# Security Policy

## Supported Versions

Motus Work Ledger is currently an alpha specification and conformance surface.
Security-relevant fixes apply to the current `main` branch and the latest
tagged alpha release.

| Version | Supported |
| --- | --- |
| `main` | yes |
| latest tagged alpha | yes |
| earlier alpha tags | best effort |

## Reporting A Vulnerability

Please do not report security vulnerabilities through public GitHub issues.

Report them through GitHub Security Advisories for this repository:

https://github.com/motus-os/motus-work-ledger/security/advisories

You should receive a response within 48 hours.

Include as much of the following as you can:

- affected file or schema,
- commit, tag, or release,
- reproduction steps,
- impact,
- whether the issue can leak secrets or sensitive work evidence,
- proof of concept if available.

## Security Model

Motus Work Ledger defines portable receipt and conformance rules. It is not a
hosted service and does not require raw transcript capture, screen recording,
keystroke capture, or employee activity monitoring.

Implementations should:

- prefer evidence references over embedded sensitive content,
- hash referenced evidence with declared canonicalization,
- mark redaction explicitly,
- avoid local absolute paths unless the operator opts in,
- treat actor, model, tool, instruction, and evidence metadata as sensitive,
- never persist secrets in receipts, fixtures, logs, examples, release evidence,
  or pilot closeout notes.

If a secret is accidentally committed, embedded in an artifact, or shared in a
receipt, stop using the affected material, revoke or rotate the secret, remove
or quarantine the artifact where possible, and file a private advisory.

## Repository Hardening Baseline

This repository should maintain the following GitHub controls:

- secret scanning enabled,
- secret scanning push protection enabled,
- Dependabot security updates enabled,
- Actions workflow token default permissions set to read-only,
- Actions restricted to GitHub-owned, verified, and `motus-os/*` actions,
- branch protection requiring the `conformance` status check,
- branch protection requiring pull request review and conversation resolution,
- force pushes and branch deletions disabled for `main`.

Repository secrets and variables should remain empty unless a future release
process explicitly requires them and documents why. Prefer OpenID Connect or
environment-scoped credentials over long-lived repository secrets.

## Privacy Guardrail

Motus records consequential work facts, not worker activity streams.

Motus Work Ledger must not be used to imply keystroke capture, screen recording,
employee monitoring, compliance guarantees, or raw transcript archiving.

## Dependency Policy

The validator has a small dependency surface. Routine dependency churn should
stay low. Security updates should be handled promptly and scoped to the affected
tooling.

Dependabot security updates are enabled for the validator dependency surface.
Routine version-bump PRs should stay disabled unless a specific maintenance
reason exists.

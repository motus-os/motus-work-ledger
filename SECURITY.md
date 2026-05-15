# Security Policy

## Supported Versions

Motus Work Ledger is currently an alpha specification and conformance surface.
Security-relevant fixes apply to the current `main` branch until versioned
releases begin.

| Version | Supported |
| --- | --- |
| `main` | yes |
| tagged alpha releases | best effort |

## Reporting A Vulnerability

Please do not report security vulnerabilities through public GitHub issues.

Report them through GitHub Security Advisories for this repository once the
repository is public.

Include as much of the following as you can:

- affected file or schema,
- commit, tag, or release,
- reproduction steps,
- impact,
- whether the issue can leak secrets or sensitive work evidence,
- proof of concept if available.

## Security Model

Motus Work Ledger defines portable receipt and conformance rules. It is not a
hosted service and does not require raw transcript capture.

Implementations should:

- prefer evidence references over embedded sensitive content,
- hash referenced evidence with declared canonicalization,
- mark redaction explicitly,
- avoid local absolute paths unless the operator opts in,
- treat actor, model, tool, instruction, and evidence metadata as sensitive,
- avoid persisting secrets in receipts, fixtures, logs, or examples.

## Privacy Guardrail

Motus records consequential work facts, not worker activity streams.

Motus Work Ledger must not be used to imply keystroke capture, screen recording,
employee monitoring, compliance guarantees, or raw transcript archiving.

## Dependency Policy

The validator has a small dependency surface. Routine dependency churn should
stay low. Security updates should be handled promptly and scoped to the affected
tooling.


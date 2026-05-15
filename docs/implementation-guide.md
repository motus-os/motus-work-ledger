# Implementation Guide

To emit a Motus-compatible Work Receipt:

1. create a bounded run identity,
2. record or reference ordered work events,
3. identify the actor,
4. reference evidence by digest and URI when possible,
5. declare the terminal outcome,
6. declare the acceptance status and actor,
7. add route or handoff projections when relevant,
8. compute the canonical receipt digest,
9. validate against the schema and conformance fixtures.

Start with Level 0 receipt-only conformance. Add event-backed conformance after
the receipt shape is stable.


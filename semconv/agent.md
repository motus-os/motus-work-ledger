# Agent Semantic Conventions

Agent attributes describe an AI or automation runtime when it is the actor or a
material participant.

| Attribute | Requirement | Type | Description |
| --- | --- | --- | --- |
| `agent.runtime` | Required | string | Runtime name, such as `codex`, `claude-code`, `github-action`, or `custom`. |
| `agent.session.id` | Recommended | string | Runtime-local session identifier when available. |
| `agent.instruction.ref` | Recommended | string | Reference to the instruction or prompt source used for the work. |
| `agent.model.provider` | Optional | string | Model provider name if material and safe to disclose. |
| `agent.model.name` | Optional | string | Model name or family if material and safe to disclose. |
| `agent.mode` | Optional | string | Runtime mode, such as `interactive`, `batch`, or `headless`. |

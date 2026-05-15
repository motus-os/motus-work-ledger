# Tool Semantic Conventions

Tool attributes describe tools invoked during work.

| Attribute | Requirement | Type | Description |
| --- | --- | --- | --- |
| `tool.name` | Required | string | Tool, command, API, or integration name. |
| `tool.kind` | Recommended | string | Category such as `shell`, `api`, `mcp`, `ci`, `vcs`, or `validator`. |
| `tool.call.id` | Recommended | string | Stable call identifier when available. |
| `tool.input.hash` | Recommended | digest object | Hash of canonicalized input when safe and meaningful. |
| `tool.output.hash` | Recommended | digest object | Hash of canonicalized output when safe and meaningful. |
| `tool.permissions.scope` | Optional | string | Permission scope or capability boundary used for the call. |
| `tool.exit_code` | Optional | integer | Process exit code for command-like tools. |

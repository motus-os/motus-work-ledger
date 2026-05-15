# Code Semantic Conventions

Code attributes describe source-control and code-change context.

| Attribute | Requirement | Type | Description |
| --- | --- | --- | --- |
| `code.repository` | Recommended | string | Repository identifier or URL. |
| `code.ref` | Recommended | string | Branch, tag, or ref name. |
| `code.commit.sha` | Recommended | string | Commit SHA associated with the work. |
| `code.diff.hash` | Optional | digest object | Hash of canonicalized diff when available. |
| `code.pr.number` | Optional | string | Pull request or merge request number. |
| `code.review.ref` | Optional | string | Review URL or identifier. |

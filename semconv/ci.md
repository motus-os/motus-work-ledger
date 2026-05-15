# CI Semantic Conventions

CI attributes describe continuous-integration context and results.

| Attribute | Requirement | Type | Description |
| --- | --- | --- | --- |
| `ci.provider` | Recommended | string | CI provider, such as `github-actions`, `gitlab-ci`, or `jenkins`. |
| `ci.workflow.name` | Recommended | string | Workflow or pipeline name. |
| `ci.run.id` | Recommended | string | CI run identifier. |
| `ci.job.name` | Optional | string | Job name. |
| `ci.status` | Required | enum | One of `success`, `failure`, `cancelled`, `skipped`, or `unknown`. |
| `ci.artifact.ref` | Optional | string | Artifact URL or path containing exported evidence. |
| `ci.log.ref` | Optional | string | Log URL or reference. Prefer references over embedding logs. |

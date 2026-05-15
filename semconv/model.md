# Model Semantic Conventions

Model attributes identify model metadata when it materially affects
reconstruction. They are descriptive only; Motus is not a model router.

| Attribute | Requirement | Type | Description |
| --- | --- | --- | --- |
| `model.provider` | Optional | string | Provider name when disclosed. |
| `model.name` | Optional | string | Model name or family when disclosed. |
| `model.version` | Optional | string | Model version, date, or snapshot when known. |
| `model.role` | Optional | string | Role in the work, such as `planner`, `builder`, `reviewer`, or `summarizer`. |
| `model.disclosure` | Recommended | enum | One of `disclosed`, `redacted`, `unknown`, or `not_applicable`. |

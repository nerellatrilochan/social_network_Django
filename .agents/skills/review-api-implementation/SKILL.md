---
name: review-api-implementation
description: >
  Reviews a developer's DSU / clean-architecture API implementation against the team's layered architecture standards. Use this skill whenever a developer says they've finished an API, an endpoint, or a feature and wants it reviewed — even if they don't say "review skill". Triggers on phrases like "review my API", "I'm done with the endpoint", "can you check my interactor/view/storage/presenter/model", "review my implementation", "I finished the assignment", "check my fb_post code", "does this follow clean architecture". Works for ANY endpoint in ANY app — reviews architecture (OpenAPI spec, views, interactors, storages, presenters, models, adapters, DTOs, enums, mixins, naming, security), not a specific domain.
---

# Review: Clean-Architecture API Implementation

You are reviewing a developer's API implementation against the layered ("clean architecture") standards used in this codebase. Your job is not just to find bugs — it is to help them build intuition for *why* each layer exists and *why* each rule matters.

This skill is **domain-agnostic**. Do not assume any particular models, endpoints, or enums. First infer the feature's contract from the code and OpenAPI spec, then apply the rules below.

**Before judging:** read the app's existing `api_spec.json` and neighbouring endpoints to match established patterns (field names, error shape, storage split level, presenter style). Do not impose conventions the app does not use unless they violate a rule here.

For extended checklists (ORM details, spec edge cases, service interfaces), see [references/layer-details.md](references/layer-details.md).

---

## How to Conduct the Review

1. **Gather the code** per endpoint: `api_specs/api_spec.json`, `views/<endpoint>/api_wrapper.py` + `__init__.py`, interactors, `interactors/storage_interfaces/` + `interactors/presenter_interfaces/`, `storages/`, `presenters/`, `models/`, `constants/`, `exceptions/`, `adapters/`, `interfaces/` (if inter-app), DTO files.
2. **Establish the contract** from the spec and models (inputs, outputs, every error case).
3. **Read all layers before writing findings** — flag root causes, not symptoms.
4. **Write a structured report** (Output Format below). Every finding: location, problem, why it matters, concrete fix.
5. **Severity:** Critical (architecture break / runtime error / security) · Major (scale / maintainability) · Minor (style).
6. **Score each layer and compute the final score** using the Scoring Rules below — severity ratings drive the deductions, so settle severity before scoring.
7. **Persist the report** (see Persisting Reports below) so reviews accumulate as an auditable history, then show the same report in the chat response.
8. **Be educational.** Respect the **Do Not Flag** list — false positives erode trust.

---

## Output Format

```
## API Review — <Endpoint / Feature Name>

### Summary
### [L1] OpenAPI Spec — Score: X/10
### [L2] Views — Score: X/10
### [L3] Interactors — Score: X/10
### [L4] Storages — Score: X/10
### [L5] Presenters — Score: X/10
### [L6] Models — Score: X/10
### [L7] Adapters — Score: X/10
### [L8] Naming, DTOs & Enums — Score: X/10
### [L9] Code Patterns & Security — Score: X/10

### What Was Done Well
### Priority Fix Order

### Score Report
<Table: Layer | Score | Deductions summary>
**Final Score: X/10 — <verdict>**
```

Write `No issues found` for clean layers. Skip L7 only when no adapters apply (mark it `N/A` and exclude it from the final score).

### Persisting Reports

Save every review as a markdown file so developers and leads can track scores across iterations without digging through chat history:

- **Location:** `review_reports/` inside the reviewed app (e.g. `fb_post/review_reports/`). Create the directory if it doesn't exist. If the code was pasted inline with no app directory to write into, use `review_reports/` at the workspace root instead.
- **Filename:** `<endpoint_or_scope>_<YYYY-MM-DD_HHMM>.md` (e.g. `create_post_2026-07-02_0946.md`, or `all_apis_2026-07-02_0946.md` for a whole-app review). The timestamp keeps successive reviews of the same endpoint side by side, so re-reviews after fixes show score progression.
- **Content:** the full report, exactly as shown in the chat — findings, per-layer scores, Score Report table, and final verdict. Prepend a small metadata header:

```markdown
---
reviewed_app: <app_name>
scope: <endpoint(s) reviewed>
date: <YYYY-MM-DD HH:MM>
final_score: <X/10>
verdict: <verdict band>
---
```

The `final_score` in the header lets anyone grep across `review_reports/` to see all scores at a glance (e.g. `grep -r "final_score" */review_reports/`).

### Scoring Rules

Score each layer out of 10. Start at 10 and deduct per finding:

- **Critical** finding → −4
- **Major** finding → −2
- **Minor** finding → −0.5

Floor each layer at 0. A layer with `No issues found` scores 10.

**Final score** = weighted average of the applicable layers (skip `N/A` layers, renormalising weights):

| Layer | Weight |
|-------|--------|
| L3 Interactors | 20% |
| L4 Storages | 15% |
| L1 OpenAPI Spec | 12% |
| L5 Presenters | 12% |
| L6 Models | 12% |
| L2 Views | 10% |
| L8 Naming, DTOs & Enums | 8% |
| L9 Code Patterns & Security | 8% |
| L7 Adapters | 3% |

Weights reflect where architecture violations hurt most: interactors own the business logic and storages own data access, so mistakes there dominate. If L9 contains a **security** finding (user id from request body, hardcoded secrets, PII leaks), cap the final score at 5/10 regardless of the weighted average — a security hole is never acceptable.

**Verdict bands:**
- **9–10** — Excellent: merge-ready, follows architecture faithfully
- **7–8.9** — Good: minor cleanup needed, no structural issues
- **5–6.9** — Needs work: fix majors before merge
- **3–4.9** — Significant rework: architecture violations present
- **0–2.9** — Restructure: fundamental layer-contract breaks

In the Score Report table, list each layer's score with a one-line deduction summary (e.g. "8/10 — 1 Major: N+1 in comment loop") so the developer sees exactly where the points went.

---

## App Folder Structure

```
app_name/
├── api_specs/api_spec.json
├── views/<endpoint>/
│   ├── api_wrapper.py          # ← editable
│   ├── __init__.py             # ← editable (API_ENVIRONMENT = "ENV_IMPL")
│   ├── validator_class.py      # auto-generated — do not edit
│   └── request_response_mocks.py
├── interactors/
│   ├── <feature>_interactor.py
│   ├── mixins/                 # inherited, not composed
│   ├── storage_interfaces/     # ABC + dtos.py per aggregate (or single StorageInterface)
│   └── presenter_interfaces/   # one ABC per endpoint
├── storages/                   # implementations — only layer importing models
├── presenters/                 # one implementation per endpoint + mixins/
├── adapters/                   # <service>_service_adapter.py + service_adapter.py + dtos.py
├── interfaces/                 # ServiceInterface — exposes app to other Django apps
├── models/  (or models.py)     # schema only — no query logic
├── constants/                  # enums.py, exception_messages.py, config.py, constants.py
├── exceptions/custom_exceptions.py
├── utils/                      # third-party HTTP services, sheet loaders, AWS helpers
├── migrations/
└── tests/
```

**Storage / model file split:** default is a single `storage_implementation.py` + `StorageInterface` and a single `models.py`. Split per aggregate/entity only when the app already does so or the single file is genuinely hard to navigate — never require a split for a small feature. Match the app's existing pattern.

Interfaces live under `interactors/`; implementations in top-level `storages/` and `presenters/`. Never edit the project `build/` folder.

---

## The Layer Contract

**View → Interactor → Storage/Adapter → Interactor → Presenter → HttpResponse**

| Layer | Owns | Must never |
|-------|------|------------|
| View | param extraction, wiring | business logic, ORM, try/except |
| Interactor | business logic, validation | import models, build HttpResponse |
| Storage | ORM queries → DTOs | business rules, logging |
| Adapter | external/inter-app calls → local DTOs | business logic |
| Presenter | DTO → HttpResponse | raise, storage calls, logic |

**Swap test:** could you replace storage with a fake, or call the interactor core from a sheet loader / `ServiceInterface` without changing it?

---

## Layer Review Rules

### [L1] OpenAPI Spec

Swagger **2.0** only (`definitions`, `parameters`, `responses`, `allOf` — no OpenAPI 3.x).

- No `success`/`status`/`error` wrapper fields in bodies — HTTP status codes carry outcome.
- **POST** for create/update/delete/actions (body required, even if empty). **GET** for read-only. No `PATCH`/`PUT`/`DELETE` unless assignment requires it. Filters in POST body; only pagination in query params.
- Paths: `/entity/action/v1/` — no actor/screen segments, no verb duplicating the HTTP method.
- **Invalid input → `400`**, including unknown/invalid ids ("invalid post id", not "not found" with `404`). **`403`** only for authorization on a valid resource.
- Error body: `response`, `http_status_code`, `res_status`. Every `res_status` the code can raise must be in the spec.
- Datetimes: `type: "string"`, no `format: "date-time"`. No `x-nullable: true` — use `required` array.
- OAuth: GET → `[{ "oauth": ["read"] }]`, POST mutations → `[{ "oauth": ["write", "read"] }]`.
- List endpoints: return list + total count. See [layer-details.md](references/layer-details.md) for nested paths, derived values, enum-in-body rules.

---

### [L2] Views (`api_wrapper.py`)

Thin adaptor only.

- `user_id` from `kwargs['user'].user_id` — **never** from `request_data` (security).
- Other params: `kwargs['request_data']`, path params: `kwargs['path_params']`.
- Instantiate storage impl(s) + presenter impl + interactor → call `interactor.<op>_wrapper(..., presenter=presenter)`.
- Storage(s) → interactor constructor. Presenter → per-call to wrapper. Adapters → via `get_service_adapter()` inside interactor only.
- `__init__.py`: `API_ENVIRONMENT = "ENV_IMPL"`.
- **Absolute imports only** — no `from .module import ...`.

---

### [L3] Interactors

**Wrapper + core** per operation. **Interactor never knows HTTP:**
- No `from django.http import HttpResponse`.
- No `-> HttpResponse` on the wrapper (presenter owns the HTTP type).
- Wrapper: try/except per domain exception → `return presenter.<error_method>()`; success → `return presenter.get_<resource>_<op>_response(...)`. No business logic. No bare `except Exception`. No docstring on wrapper.
- Core: business logic; raises domain exceptions; returns typed DTOs (primitives like `int` id are fine). Docstring with behaviour + exceptions. No model imports. No storage/adapter calls in loops.

```python
class CreateResourceInteractor:
    def __init__(self, resource_storage: ResourceStorageInterface):
        self.resource_storage = resource_storage

    def create_resource_wrapper(
        self, user_id: str, content: str,
        presenter: CreateResourcePresenterInterface,
    ):
        try:
            resource_id = self.create_resource(user_id=user_id, content=content)
        except InvalidContentException:
            return presenter.raise_invalid_content_exception()
        return presenter.get_create_resource_response(resource_id=resource_id)

    def create_resource(self, user_id: str, content: str) -> int:
        ...
```

- Inject only needed storages. `get_service_adapter().<svc>.<method>()` inline — never store adapter on `self`, never import adapter classes directly.
- No per-call state on `self` (`self.x = ...` between methods).
- Validate cheapest-first (enum, empty string) before DB, always before writes.
- No redundant storage calls — see [layer-details.md](references/layer-details.md).
- Concurrency: handle `IntegrityError` or use `get_or_create` / `select_for_update()` in `transaction.atomic()`.
- **Sheet-loading:** no wrapper, no presenter — util calls core directly.
- **`interfaces/service_interface.py`:** must call interactor **core** method, never wrapper or storage directly.

---

### [L4] Storages

Only layer importing models. Always returns DTOs — never models, dicts, or QuerySets.

Match app's split level (single file or per-aggregate). Each impl has `_to_dto` when conversion repeats.

Key rules (full list in [layer-details.md](references/layer-details.md)):
- `.get()` → `DoesNotExist` → domain exception (not `None` unless explicitly optional-by-contract).
- N+1: bulk-fetch + `{id: dto}` maps; `select_related` / `prefetch_related` when DTO uses relations.
- `.exists()` not count; `obj.fk_id` not `obj.fk.id`; `bulk_create`/`bulk_update(batch_size=1000)`; `F()` for atomic increments.
- Race: `get_or_create` / `IntegrityError` handler. `select_for_update` inside `atomic()`.
- One queryset pipeline per method; no business/conditional-write logic; no logging.
- Assumes interactor validated preconditions.

---

### [L5] Presenters

One presenter per endpoint. Interface methods return `-> HttpResponse`.

**Inherit `HTTPResponseMixin`** (`dsu.runtime.mixin.http_response_mixin` or `django_swagger_utils.utils.http_response_mixin`):
- Success: `return self.prepare_200_success_response(response_dict)` (or `prepare_201_*`).
- Errors: build `{response, http_status_code, res_status}` → `return self.prepare_400_bad_request_response(...)`. Prefer **`400`** for invalid input.
- Error method names: `get_invalid_<x>_response()` or `raise_<x>_exception()` — both valid if they use `prepare_*`.
- Shared logic in **inherited** mixins (`presenters/mixins/`) — error mixin + serializer mixin. Never `self.mixin = X()`.
- `convert_datetime_to_local_string()` on all datetimes; `[]` not `None` for list fields; keys match spec exactly.

Flag raw `HttpResponse(json.dumps(...))` when `HTTPResponseMixin` is the app convention.

---

### [L6] Models

`AbstractDateTimeModel` base. Schema + validators only — queries live in storage.

**Users:** no local `User` model. `AUTH_USER_MODEL = 'ib_users.UserAccount'`. Store `<role>_id = CharField(max_length=36)`; fetch profiles via ib_users adapter.

**FKs:** `on_delete` + `related_name`; optional FKs `null=True`; string refs for circular imports.

**Enums on fields:** `validators=[validate_<enum>]` using `Enum.get_list_of_values()` — not `choices` alone.

**Naming:** nouns only — no verbs, actors, UI labels in model/enum names. Status enums (not booleans) for lifecycle with 3+ foreseeable states.

**MySQL:** no `JSONField`/`ArrayField`/`GENERATED`; JSON → `TextField` + property. `unique_together` where domain requires. See [layer-details.md](references/layer-details.md) for soft-delete, null+blank, enum defaults.

---

### [L7] Adapters

Only path to other apps/services. Returns **local** DTOs.

- Per-service adapter file + aggregator `ServiceAdapter` with lazy `@property` per service + `get_service_adapter()`.
- Convert external DTOs at adapter boundary — never pass through another app's types.
- Bulk-fetch (e.g. `get_user_profiles_bulk`), not per-id in a loop.
- For `ib_users`: adapter may route via `IS_IB_USER_ACCOUNT` / `IS_IB_USERS_SSO` settings to the correct service interface.
- Third-party HTTP: logic in `utils/` service class, adapter delegates. boto3 (S3/SES/SNS): infra-native, explicit creds+region from settings, no adapter required.
- Catch client exceptions → domain exception; `logger.warning()` only.

---

### [L8] Naming, DTOs & Enums

**Extraction test:** strip actors, UI labels, transient attributes, tool names — what remains is the name.

- Interactors: `<Verb><Resource>Interactor`; storage: `<verb>_<resource>_<qualifier>`; existence: `does_<x>_exist`.
- Presenters: `get_<resource>_<op>_response`.
- DTOs: `<Domain><Context>DTO`, vars end `_dto`, fields match model names. No `Optional[X] = None` defaults. Max ~10 fields; nesting ≤ 2 levels. Do not mutate a DTO after storage returns it if reused.
- Enums: `constants/enums.py`, `*Enum`/`*Status`, `BaseEnumClass`, valid identifiers (`THUMBS_UP` not `THUMBS-UP`). Validate via enum, not hardcoded lists.
- Variables: plural not `_list`; `<key>_to_<value>` not `_dict`; boolean prefix `is_`/`has_`/`can_`.
- No `_v2`/`_v3` suffixes on code identifiers (path `/v2/` OK for coexistence).
- `config.py` = env-specific; `constants.py` = fixed business literals; `exception_messages.py` = `(message, res_status)` tuples.

---

### [L9] Code Patterns & Security

- Type hints on all args/returns except interactor wrapper return. Functions >25 lines deserve scrutiny; >35 split. Nesting >3 levels → extract helper.
- No flag arguments routing structurally different branches — split methods instead.
- `get_current_local_date_time()` not `datetime.now()`. Use `defaultdict` over manual key-init loops.
- No silent suppression (`except: pass`, `errors="ignore"` without re-raise+log).
- DB write then external call: flag if external failure leaves inconsistent committed state.
- `django.conf.settings` not `os.environ` in app code. No hardcoded secrets. No `os.system()`. No PII in logs/responses.
- Log once at termination; never log-then-reraise. Logger at module level.

---

## Cross-Cutting

- **Mixins:** inherited (`class X(Mixin):`), never composed (`self.mixin = Mixin()`).
- **Cross-app isolation:** redefine enums/DTOs/exceptions locally — importing from another app's module is a violation (unless explicit extension app).
- **Reuse before creating:** check existing exceptions, DTOs, utils.
- **Extract to utils/** only when ~15+ lines, generic, and business logic — not 2–3 line wrappers.

---

## Completeness Checklist (per endpoint)

- [ ] Spec entry with all error cases (`400` for invalid input)
- [ ] `ENV_IMPL` in view `__init__.py`
- [ ] `api_wrapper.py` wires layers correctly
- [ ] Interactor: wrapper (no HttpResponse) + core (typed DTOs, docstring)
- [ ] Storage interface + impl; only storage touches models
- [ ] Per-endpoint presenter + interface; `HTTPResponseMixin`; mixins for shared logic
- [ ] DTOs at every boundary; ib_users via adapter; no local User model
- [ ] Exceptions + enums + model validators in place

---

## Common Mistakes

1. `user_id` from `request_data` not `kwargs['user'].user_id`
2. `HttpResponse` imported or return-annotated in interactor
3. `404` for invalid/unknown id — use `400`
4. Hand-rolled `User` model instead of `ib_users` + `<role>_id` + adapter
5. Interactor imports/queries models
6. Presenter in interactor constructor
7. Monolithic presenter when app uses per-endpoint pattern (or vice versa)
8. Storage/adapter calls inside loops (N+1)
9. Storage returns models; core returns raw tuples/dicts
10. Raw `HttpResponse(json.dumps(...))` instead of `HTTPResponseMixin.prepare_*`
11. Enum field unvalidated or hardcoded string list in interactor
12. `Optional[X] = None` DTO defaults
13. Raw `datetime` in presenter without `convert_datetime_to_local_string()`
14. `ENV_MOCK` left in `__init__.py`
15. Business validation in storage (`validate_*`)
16. `self.x = ...` per-call state on interactor
17. External DTOs leaking past adapter
18. Importing another app's types
19. `ServiceInterface` calling wrapper or storage instead of interactor core
20. Editing auto-generated view files or `build/`

---

## Do Not Flag

- Docstring presence/absence on non-core methods
- TODO comments
- Import ordering / inline imports
- Missing auth checks (OAuth handled by DSU before `api_wrapper`)
- Missing `from err` chaining
- Cross-app local redefinition of identical enum/DTO/exception
- HTTP logic in adapters when that app consistently does so
- API path `/v2/` for coexistence
- Inline 2–3 line helpers kept local
- Single-file storage/models when the app is small and consistent

# Layer Details — Extended Checklists

Read sections here when the main SKILL.md rule needs more depth for a finding.

## OpenAPI Spec — Extended

- **Align first**: read the app's existing `api_spec.json` before judging a new endpoint. Match field names, error shape, security, and schema composition — do not import generic REST conventions from outside.
- **List endpoints**: always return the list **and** a total count field (full filtered set size, not page length).
- **Nested resources**: express parent/child as nested path segments (`user/exam/review/v1/`), never a hyphenated compound (`exam-review`, `mark-as-solved`).
- **Caller context**: values that identify caller/origin belong in the request body, not as backend constants.
- **Derived values**: non-trivial computation (percentages, eligibility, aggregations) belongs in the backend; trivial display formatting (`full_name` from first+last) stays on the frontend.
- **State fields**: use enums for lifecycle/state even with only two values today; reserve booleans for genuinely binary facts (`is_deleted`, `is_verified`).
- **Error responses**: every `res_status` the interactor can produce must appear in the spec's error response `enum` array.

## Storage ORM — Extended

- **`.get()`**: wrap in `try/except ObjectDoesNotExist` → raise domain exception. Do not catch `DoesNotExist` and return `None` unless the method contract is explicitly optional lookup by design.
- **UUID fields**: convert to `str` in DTOs.
- **`.values()` / `.values_list()`**: convert queryset results to plain `list` before returning.
- **Existence**: use `.exists()`, not `.count() > 0`.
- **FK ids**: read `obj.blog_id`, not `obj.blog.id`.
- **Ordering**: add `.order_by()` only when required; do not set `Meta.ordering` on models.
- **Queryset reuse**: evaluate/cache before iterating twice.
- **`bulk_update`**: pass explicit `fields=[...]` including `last_update_datetime`, set to `get_current_local_date_time()`.
- **`bulk_create`**: use `batch_size=1000`; no `avoid_conflicts`; prefer separate create/update methods over upsert.
- **Soft delete**: `update(is_deleted=True, ...)` not `.delete()` when the model uses soft delete.
- **One query per method**: each storage method runs one queryset pipeline; multi-step orchestration belongs in the interactor.
- **No conditional writes in storage**: e.g. `first_solved = existing.x or new_x` — interactor computes, storage persists.
- **DB functions**: avoid `django.db.models.functions` unless ORM + Python cannot do it; comment if used.
- **`select_related` / `prefetch_related`**: only when returned DTO actually uses those relations.

## Models — Extended

- `null=True` fields should also have `blank=True`.
- Enum fields with an explicit initial state (`PENDING`, `DRAFT`) → use `default=` that value, not `null=True`.
- UUID primary keys only when the id is externally exposed; internal records use auto-increment int PK.
- JSON stored in `TextField` + `@property` `*_json` accessor; validate JSON before write.
- Soft-delete models: default manager filters `is_deleted=False`; `all_objects` manager for full access.
- New fields on models with existing rows need `default=` or `null=True`.
- Do not add DB indexes unless explicitly requested.

## Presenters — Extended

Both error-naming styles exist in production code — accept either if it uses `HTTPResponseMixin`:
- `get_invalid_<x>_response()` (preferred in newer code)
- `raise_<x>_exception()` (older code)

Error body shape:
```python
response = {
    "response": MESSAGE_TUPLE[0],
    "http_status_code": 400,
    "res_status": MESSAGE_TUPLE[1],
}
return self.prepare_400_bad_request_response(response)
```

Success: `return self.prepare_200_success_response(response_dict)` (or `prepare_201_*` for creates).

Import path (either is valid in the codebase):
- `from dsu.runtime.mixin.http_response_mixin import HTTPResponseMixin`
- `from django_swagger_utils.utils.http_response_mixin import HTTPResponseMixin`

## Interactors — Extended

- Wrapper method: **no docstring** required.
- Core method: docstring stating behaviour + exceptions raised.
- Never `self.adapter = get_service_adapter()` — call inline in the method that needs it.
- Never `from app.adapters.foo_adapter import FooAdapter` in an interactor.
- Private mixin methods (`_foo`) are callable only within that mixin hierarchy — not from a sibling interactor.
- Validation helpers that raise (not return bool) → name `validate_*` or `raise_if_not_*`, not `is_*` / `has_*`.
- Flag arguments (`if include_details: ... else: ...`) → split into separate methods unless it's a storage filter enum.

## App Service Interface (`interfaces/service_interface.py`)

When the app exposes methods to other Django apps:
- Instantiate storage + interactor inside the interface method.
- Call the interactor **core** method only — never the wrapper (wrapper returns HTTP).
- Never call storage directly from the interface, even for a one-line lookup.

## Imports

- Use **absolute** imports: `from myapp.interactors.storage_interfaces.post_storage_interface import PostStorageInterface`
- No relative imports (`from .storage_interfaces import ...`) in application code.

## Auto-Generated Files — Do Not Edit

- Project `build/` folder (urls, routing) — regenerated on DSU build.
- Per-endpoint view files except `api_wrapper.py` and `__init__.py` (`validator_class.py`, `request_response_mocks.py`, `<operation>.py`).

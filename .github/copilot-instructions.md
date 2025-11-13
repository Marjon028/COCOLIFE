## Purpose
This file provides concise, actionable guidance for AI coding agents to be immediately productive in this Django + DRF codebase.

## Big picture (what this project is)
- Django 5.2 project (root `manage.py`, settings in `cocolife/settings.py`).
- Single app: `Product_Management` — exposes a REST API under `/api/` (see `cocolife/urls.py`).
- Persistence: local SQLite (`db.sqlite3`).
- Media files are stored under `media/` (configured in `settings.py`) and served in DEBUG (`cocolife/urls.py`).

## Major components & boundaries
- `Product_Management/models.py` contains the domain models: Product, ProductInfo, ProductInfoImage, PolicyOwner, PolicyOwnerData, PolicyOwnerPdfFile, TypeOfNeed.
  - Many fields use JSONField for flexible structured data (e.g. `PolicyOwner.title`, `ProductInfo.product_description`).
  - Relationships:
    - `Product` -> OneToOne `PolicyOwner` (product contains policy-owner metadata)
    - `ProductInfo` -> many `ProductInfoImage` (images stored with ImageField)
    - `PolicyOwner` -> OneToOne `PolicyOwnerPdfFile`

## API surface and patterns
- Router lives in `Product_Management/urls.py` with ModelViewSets in `Product_Management/views.py`.
- Key endpoints (via DRF router):
  - `GET /api/product-info/` (ProductInfoViewSet) — contains nested read-only `product_images`.
  - `POST /api/product-info/{id}/upload-images/` — custom action that accepts multipart `images` (list) and `alt_texts` (list).
  - `GET/POST /api/policy-owners/` — `PolicyOwnerViewSet` implements a custom `list()` that returns a default JSON structure when no DB entries exist.

## Notable code patterns (important to preserve)
- Default JSON helpers: `default_policy_owner_data()` and `default_address()` in `models.py` — used to create default JSON structures and to initialize serializer `get_initial()` (see `serializers.py`).
- `perform_create()` used to attach `user` from `request` in several viewsets (`ProductInfoViewSet`, `PolicyOwnerDataViewSet`).
- Nested serializers: `ProductInfoSerializer` returns nested `product_images` via `ProductInfoImageSerializer` (read-only).
- Authentication: `rest_framework.authtoken` is in `INSTALLED_APPS` but token auth is commented out in several viewsets — enabling auth requires uncommenting `authentication_classes` and `permission_classes` in the view classes.

## Common developer workflows (commands)
Use PowerShell on Windows. From project root (`manage.py`):

```powershell
# create & activate venv (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# install runtime deps
pip install -r requirements.txt

# create migrations (if models change)
python manage.py makemigrations
python manage.py migrate

# create admin user
python manage.py createsuperuser

# run development server (media served in DEBUG)
python manage.py runserver

# run tests
python manage.py test
```

## Examples & usage notes the agent should use
- Upload multiple images: send multipart POST to `/api/product-info/{id}/upload-images/` with files under `images` and optional `alt_texts` list; the view creates `ProductInfoImage` objects and returns them serialized.
- When returning policy-owner structure for empty DB, `PolicyOwnerViewSet.list()` returns the default structure (useful for front-end initialization).
- When editing or creating `ProductInfo`, the serializer expects `user` to be attached via `perform_create()` (server-side), so POSTs generally omit `user` field.

## Project-specific gotchas / things to watch
- Many fields are JSONField and can be null — code relies on default JSON shapes. When generating patches or tests, use the `default_policy_owner_data()` and `default_address()` shapes to avoid validation surprises.
- `ProductInfoSerializer.create()` contains a check `if user.is_admin: raise ValidationError("User must be authenticated to create ProductInfo.")` — this is unusual. When modifying authentication logic verify intent (likely a bug or reversed condition).
- Token auth is present but not enforced. If you enable TokenAuthentication, update client workflows and tests accordingly.
- Media upload paths: `terms_and_conditions/` and `product_info_images/` live under `media/`. When testing uploads, ensure the test client uses `multipart/form-data` and the test environment cleans up files (or use in-memory storage for tests).

## Files to inspect when making changes
- Models & defaults: `Product_Management/models.py`
- API surface: `Product_Management/views.py`, `Product_Management/serializers.py`, `Product_Management/urls.py`
- Admin and quick DB inspection: `Product_Management/admin.py`
- Project settings & media routing: `cocolife/settings.py`, `cocolife/urls.py`
- Dependencies: `requirements.txt`

## When to ask the human
- If your change touches authentication or user ownership logic (e.g., `perform_create`, `user` fields), ask which access model is intended.
- If you plan to change the JSON schema stored in JSONFields, ask whether migration / backfill is required.

---
If you'd like, I can iterate on this file to include quick code snippets (unit test stubs for image upload and PolicyOwner default behavior) or enable-auth migration steps. Any unclear parts to expand? 

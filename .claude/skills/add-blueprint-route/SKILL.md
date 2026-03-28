---
name: add-blueprint-route
description: Add a new Flask Blueprint route module to SkillBoard. Use when creating a new route file, adding a new page or API endpoint group, or extending the app with a new Blueprint.
argument-hint: <domain-name>
disable-model-invocation: true
---

# Add Blueprint Route

Create a new Flask Blueprint for `$ARGUMENTS` in the SkillBoard project.

## Steps

### 1. Create the route file

Create `app/routes/$ARGUMENTS.py`.

### 2. Set up the Blueprint

```python
from flask import Blueprint, flash, redirect, render_template, request, url_for

$ARGUMENTS_bp = Blueprint("$ARGUMENTS", __name__)
```

Blueprint naming convention: `<domain>_bp` (e.g., `settings_bp`, `admin_bp`). The first argument to `Blueprint()` is the endpoint namespace — use the same domain name.

### 3. Add route handlers

Add route functions decorated with `@$ARGUMENTS_bp.route(...)`. Follow these conventions:

- Business logic belongs in `app/services/`, not in route handlers — routes should delegate to service functions
- Use `@login_required` from `flask_login` for authenticated routes
- Templates go in `app/templates/$ARGUMENTS/` subdirectory
- GET+POST routes: check `request.method`, validate form data, flash errors, render on failure, redirect on success
- Use `url_for("$ARGUMENTS.<function_name>")` for internal links

### 4. Register in the app factory

In `app/__init__.py`, inside `create_app()`:

1. Add the import alongside the other blueprint imports:
   ```python
   from app.routes.$ARGUMENTS import $ARGUMENTS_bp
   ```

2. Register the blueprint alongside the others:
   ```python
   app.register_blueprint($ARGUMENTS_bp)
   ```

### 5. Create the template directory

Create `app/templates/$ARGUMENTS/` and add the required template files.

## Reference

See existing blueprints in `app/routes/` (auth.py, profile.py, leaderboard.py, compare.py) for working examples.

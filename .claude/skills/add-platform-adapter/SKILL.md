---
name: add-platform-adapter
description: Add a new platform integration to SkillBoard following the PlatformAdapter pattern. Use when creating a new platform adapter in app/platforms/, connecting a new external API, or extending the platform registry.
argument-hint: <platform-name>
disable-model-invocation: true
---

# Add Platform Adapter

Create a new platform adapter for `$ARGUMENTS` in the SkillBoard project. Platform adapters fetch user data from external APIs and compute normalized scores for the unified profile.

## Steps

### 1. Create the adapter file

Create `app/platforms/$ARGUMENTS.py` (use snake_case for the filename).

Start with a module docstring:

```python
"""$ARGUMENTS platform adapter."""
```

### 2. Add imports

```python
import math

from .base import DEFAULT_TIMEOUT, PlatformAdapter, PlatformError, UserNotFoundError, session
from . import register
```

Use `session` (the shared requests session from base.py) for all HTTP calls — it has retry logic and a proper User-Agent already configured.

### 3. Define the adapter class

```python
class <PlatformName>Adapter(PlatformAdapter):
    slug = "$ARGUMENTS"          # snake_case DB key
    label = "<Platform Name>"    # Human-readable UI label
```

### 4. Implement `fetch(username)`

Hit the platform's public API and return a raw data dict. Key rules:

- Use `session.get()` or `session.post()` with `timeout=DEFAULT_TIMEOUT`
- Raise `UserNotFoundError` if the user doesn't exist (check for 404 or empty response)
- Let other HTTP errors propagate via `resp.raise_for_status()`
- Return a flat dict of raw metrics (ratings, counts, ranks — whatever the API provides)

```python
def fetch(self, username: str, **kwargs) -> dict:
    # Hit the API, parse response, return raw data
    ...
```

### 5. Implement `compute_scores(data)`

Convert raw data into the standard scoring format. The return value must be:

```python
{
    "power_score": int,  # 0-1000, derived from average percentile * 10
    "metrics": {
        "metric_name": {"value": <raw_value>, "percentile": <0-99.9>},
        ...
    }
}
```

Scoring approach:
- Use **logistic percentile approximations** (`1 / (1 + math.exp(-k * (x - midpoint)))`) rather than real population data
- Estimate reasonable midpoint (median) and steepness (k) for each metric
- Cap percentiles at 99.9
- Average the percentiles of active metrics (value > 0), multiply by 10 for power_score
- Return `power_score: 0` if no active metrics

### 6. Register the adapter

At module level, after the class definition:

```python
register(<PlatformName>Adapter())
```

### 7. Add to the registry imports

In `app/platforms/__init__.py`, add the new module to the import line:

```python
from . import chess_com, github, $ARGUMENTS  # noqa: E402, F401
```

## Reference

Look at `app/platforms/chess_com.py` and `app/platforms/github.py` for working examples of this pattern.

---
name: scoring-conventions
description: SkillBoard scoring and percentile conventions for platform adapters. Apply when writing or modifying compute_scores() methods, percentile functions, or power_score calculations in app/platforms/.
user-invocable: false
---

# Scoring & Percentile Conventions

Standards for how SkillBoard computes scores across all platform adapters.

## Output Format

Every `compute_scores(data)` method must return this exact structure:

```python
{
    "power_score": int,       # 0-1000
    "metrics": {
        "metric_name": {
            "value": <raw_value>,       # Original number from the API
            "percentile": <float>,      # 0-99.9
        },
        ...
    }
}
```

Additional keys (like `best_rating`) are allowed alongside `power_score` and `metrics`.

## Power Score Calculation

1. Collect all metrics where `value > 0` (these are "active" metrics)
2. Average their percentiles
3. Multiply by 10 and cast to int

```python
active = {k: v for k, v in metrics.items() if v["value"] > 0}
if not active:
    return {"power_score": 0, "metrics": metrics}
avg_percentile = sum(v["percentile"] for v in active.values()) / len(active)
power_score = int(avg_percentile * 10)
```

If no metrics are active, `power_score` is 0.

## Percentile Approximation Methods

SkillBoard uses self-contained approximations rather than real population data. Two approaches are used:

### Logistic Curves (preferred for ratings and counts with a known median)

```python
p = 1 / (1 + math.exp(-k * (x - midpoint)))
return min(p * 100, 99.9)
```

- `midpoint`: estimated population median for the metric
- `k`: steepness — controls how quickly percentiles change around the midpoint
- Used by: Chess.com ratings, LeetCode solved counts

### Logarithmic Curves (for long-tail distributions like stars/followers)

```python
if value == 0:
    return <low_baseline>   # e.g., 10.0 or 15.0
return min(base + factor * math.log10(max(value, 1)) * 2, cap)
```

- Gives a low baseline for zero values (not 0 — having an account counts for something)
- Used by: GitHub stars, repos, followers

## Rules

- Cap all percentiles at 99.9 (use 99.0 for less discriminating metrics)
- Zero-value metrics should return a low percentile (0-15), not exactly 0, unless the metric truly means "no participation"
- Keep percentile functions as private methods (`_metric_name_pct` or `_percentile`) on the adapter class
- Document the assumed distribution in a docstring on each percentile function (median, 90th, 99th estimates)
- Each metric gets its own percentile function — do not reuse one curve for different metric types

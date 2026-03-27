"""Head-to-head comparison logic."""

from app.models import User


def build_comparison(user1: User, user2: User) -> dict:
    """Compare two users on shared platforms only.

    Returns dict with shared_platforms, comparisons (per-platform metric breakdowns),
    and score (win counts for each user).
    """
    p1 = user1.platform_dict()
    p2 = user2.platform_dict()
    shared = set(p1.keys()) & set(p2.keys())

    if not shared:
        return {"shared_platforms": [], "comparisons": [], "score": [0, 0]}

    comparisons = []
    score = [0, 0]

    for platform in sorted(shared):
        s1 = p1[platform].scores or {}
        s2 = p2[platform].scores or {}
        m1 = s1.get("metrics", {})
        m2 = s2.get("metrics", {})

        platform_metrics = []
        for metric_key in sorted(set(m1.keys()) | set(m2.keys())):
            v1 = m1.get(metric_key, {})
            v2 = m2.get(metric_key, {})
            val1 = v1.get("value", 0)
            val2 = v2.get("value", 0)
            winner = 1 if val1 > val2 else (2 if val2 > val1 else 0)
            if winner == 1:
                score[0] += 1
            elif winner == 2:
                score[1] += 1

            platform_metrics.append({
                "name": metric_key,
                "value1": val1, "value2": val2,
                "pct1": v1.get("percentile", 0), "pct2": v2.get("percentile", 0),
                "winner": winner,
            })

        comparisons.append({
            "platform": platform,
            "metrics": platform_metrics,
            "power1": s1.get("power_score", 0),
            "power2": s2.get("power_score", 0),
        })

    return {"shared_platforms": sorted(shared), "comparisons": comparisons, "score": score}

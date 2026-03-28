"""LeetCode platform adapter."""

import math

from .base import DEFAULT_TIMEOUT, PlatformAdapter, PlatformError, UserNotFoundError, session
from . import register


class LeetCodeAdapter(PlatformAdapter):
    slug = "leetcode"
    label = "LeetCode"

    def fetch(self, username: str, **kwargs) -> dict:
        url = "https://leetcode.com/graphql"
        query = """
        query userProfile($username: String!) {
            matchedUser(username: $username) {
                submitStats {
                    acSubmissionNum {
                        difficulty
                        count
                    }
                }
                profile {
                    ranking
                    reputation
                }
            }
        }
        """
        resp = session.post(
            url,
            json={"query": query, "variables": {"username": username}},
            timeout=DEFAULT_TIMEOUT,
        )
        resp.raise_for_status()
        data = resp.json()

        user = data.get("data", {}).get("matchedUser")
        if not user:
            raise UserNotFoundError(f"LeetCode user '{username}' not found")

        submissions = {
            item["difficulty"]: item["count"]
            for item in user["submitStats"]["acSubmissionNum"]
        }

        return {
            "easy_solved": submissions.get("Easy", 0),
            "medium_solved": submissions.get("Medium", 0),
            "hard_solved": submissions.get("Hard", 0),
            "total_solved": submissions.get("All", 0),
            "ranking": user["profile"]["ranking"] or 0,
            "reputation": user["profile"]["reputation"] or 0,
        }

    def compute_scores(self, data: dict) -> dict:
        metrics = {
            "total_solved": self._solved_metric(data.get("total_solved", 0)),
            "hard_solved": self._hard_metric(data.get("hard_solved", 0)),
            "ranking": self._ranking_metric(data.get("ranking", 0)),
        }

        active = {k: v for k, v in metrics.items() if v["value"] > 0}
        if not active:
            return {"power_score": 0, "metrics": metrics}

        avg_percentile = sum(v["percentile"] for v in active.values()) / len(active)
        return {
            "power_score": int(avg_percentile * 10),
            "metrics": metrics,
        }

    def _solved_metric(self, count: int) -> dict:
        """Logistic curve: median ~50 solved, 90th ~300, 99th ~800."""
        p = 1 / (1 + math.exp(-0.015 * (count - 50)))
        return {"value": count, "percentile": min(p * 100, 99.9)}

    def _hard_metric(self, count: int) -> dict:
        """Logistic curve: median ~5 hard, 90th ~50, 99th ~150."""
        p = 1 / (1 + math.exp(-0.04 * (count - 5)))
        return {"value": count, "percentile": min(p * 100, 99.9)}

    def _ranking_metric(self, ranking: int) -> dict:
        """Lower ranking is better. Approximate percentile from rank."""
        if ranking == 0:
            return {"value": 0, "percentile": 0}
        total_users = 1_000_000
        p = max(0, (1 - ranking / total_users)) * 100
        return {"value": ranking, "percentile": min(p, 99.9)}


register(LeetCodeAdapter())

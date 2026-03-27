"""Chess.com platform adapter."""

import math

from .base import DEFAULT_TIMEOUT, PlatformAdapter, UserNotFoundError, session
from . import register


class ChessComAdapter(PlatformAdapter):
    slug = "chess_com"
    label = "Chess.com"

    def fetch(self, username: str, **kwargs) -> dict:
        base = f"https://api.chess.com/pub/player/{username}"

        resp = session.get(base, timeout=DEFAULT_TIMEOUT)
        if resp.status_code == 404:
            raise UserNotFoundError(f"Chess.com user '{username}' not found")
        resp.raise_for_status()

        stats_resp = session.get(f"{base}/stats", timeout=DEFAULT_TIMEOUT)
        stats_resp.raise_for_status()
        stats = stats_resp.json()

        def get_rating(mode):
            return stats.get(mode, {}).get("last", {}).get("rating", 0)

        return {
            "rapid_rating": get_rating("chess_rapid"),
            "blitz_rating": get_rating("chess_blitz"),
            "bullet_rating": get_rating("chess_bullet"),
            "puzzle_rating": (
                stats.get("tactics", {}).get("highest", {}).get("rating", 0)
                or stats.get("puzzles", {}).get("best", {}).get("rating", 0)
            ),
        }

    def compute_scores(self, data: dict) -> dict:
        metrics = {
            "rapid": self._metric(data.get("rapid_rating", 0)),
            "blitz": self._metric(data.get("blitz_rating", 0)),
            "bullet": self._metric(data.get("bullet_rating", 0)),
            "puzzle": self._metric(data.get("puzzle_rating", 0)),
        }

        active = {k: v for k, v in metrics.items() if v["value"] > 0}
        if not active:
            return {"power_score": 0, "metrics": metrics}

        avg_percentile = sum(v["percentile"] for v in active.values()) / len(active)
        return {
            "power_score": int(avg_percentile * 10),
            "metrics": metrics,
            "best_rating": max(v["value"] for v in metrics.values()),
        }

    def _metric(self, rating: int) -> dict:
        return {"value": rating, "percentile": self._percentile(rating)}

    def _percentile(self, rating: int) -> float:
        """Logistic approximation of Chess.com rating distribution.

        Median rapid ~800, 90th ~1400, 99th ~1900.
        """
        p = 1 / (1 + math.exp(-0.005 * (rating - 800)))
        return min(p * 100, 99.9)


register(ChessComAdapter())

"""Steam platform adapter."""

import math

from .base import DEFAULT_TIMEOUT, PlatformAdapter, UserNotFoundError, session
from . import register


class SteamAdapter(PlatformAdapter):
    slug = "steam"
    label = "Steam"

    API_BASE = "https://api.steampowered.com"

    def fetch(self, username: str, **kwargs) -> dict:
        api_key = kwargs.get("api_key", "")

        # Resolve vanity URL to Steam ID (64-bit)
        resolve_resp = session.get(
            f"{self.API_BASE}/ISteamUser/ResolveVanityURL/v1",
            params={"key": api_key, "vanityurl": username},
            timeout=DEFAULT_TIMEOUT,
        )
        resolve_resp.raise_for_status()
        resolve_data = resolve_resp.json().get("response", {})

        if resolve_data.get("success") == 1:
            steam_id = resolve_data["steamid"]
        elif username.isdigit() and len(username) == 17:
            steam_id = username
        else:
            raise UserNotFoundError(f"Steam user '{username}' not found")

        # Fetch profile summary
        profile_resp = session.get(
            f"{self.API_BASE}/ISteamUser/GetPlayerSummaries/v2",
            params={"key": api_key, "steamids": steam_id},
            timeout=DEFAULT_TIMEOUT,
        )
        profile_resp.raise_for_status()
        players = profile_resp.json().get("response", {}).get("players", [])
        if not players:
            raise UserNotFoundError(f"Steam user '{username}' not found")
        profile = players[0]

        # Fetch owned games with playtime
        games_resp = session.get(
            f"{self.API_BASE}/IPlayerService/GetOwnedGames/v1",
            params={"key": api_key, "steamid": steam_id, "include_played_free_games": 1},
            timeout=DEFAULT_TIMEOUT,
        )
        games_resp.raise_for_status()
        games_data = games_resp.json().get("response", {})

        games = games_data.get("games", [])
        total_playtime_minutes = sum(g.get("playtime_forever", 0) for g in games)

        # Fetch Steam level
        level_resp = session.get(
            f"{self.API_BASE}/IPlayerService/GetSteamLevel/v1",
            params={"key": api_key, "steamid": steam_id},
            timeout=DEFAULT_TIMEOUT,
        )
        level_resp.raise_for_status()
        steam_level = level_resp.json().get("response", {}).get("player_level", 0)

        return {
            "steam_id": steam_id,
            "persona_name": profile.get("personaname", username),
            "avatar_url": profile.get("avatarfull", ""),
            "games_owned": games_data.get("game_count", 0),
            "total_playtime_hours": round(total_playtime_minutes / 60, 1),
            "steam_level": steam_level,
        }

    def compute_scores(self, data: dict) -> dict:
        metrics = {
            "games_owned": self._metric(data.get("games_owned", 0), self._games_pct),
            "playtime": self._metric(data.get("total_playtime_hours", 0), self._playtime_pct),
            "steam_level": self._metric(data.get("steam_level", 0), self._level_pct),
        }

        active = {k: v for k, v in metrics.items() if v["value"] > 0}
        if not active:
            return {"power_score": 0, "metrics": metrics}

        avg_percentile = sum(v["percentile"] for v in active.values()) / len(active)
        return {"power_score": int(avg_percentile * 10), "metrics": metrics}

    def _metric(self, value, pct_fn) -> dict:
        return {"value": value, "percentile": pct_fn(value)}

    def _games_pct(self, count: int) -> float:
        """Logistic approximation — median ~50 games, 90th ~300, 99th ~1000."""
        if count == 0:
            return 0.0
        p = 1 / (1 + math.exp(-0.015 * (count - 50)))
        return min(p * 100, 99.9)

    def _playtime_pct(self, hours: float) -> float:
        """Logistic approximation — median ~200 hours, 90th ~2000, 99th ~5000."""
        if hours == 0:
            return 0.0
        p = 1 / (1 + math.exp(-0.003 * (hours - 200)))
        return min(p * 100, 99.9)

    def _level_pct(self, level: int) -> float:
        """Logistic approximation — median ~10, 90th ~50, 99th ~150."""
        if level == 0:
            return 0.0
        p = 1 / (1 + math.exp(-0.08 * (level - 10)))
        return min(p * 100, 99.9)


register(SteamAdapter())

"""GitHub platform adapter."""

import math

from .base import DEFAULT_TIMEOUT, PlatformAdapter, UserNotFoundError, session
from . import register


class GitHubAdapter(PlatformAdapter):
    slug = "github"
    label = "GitHub"

    def fetch(self, username: str, **kwargs) -> dict:
        token = kwargs.get("token")
        headers = {}
        if token:
            headers["Authorization"] = f"token {token}"

        resp = session.get(f"https://api.github.com/users/{username}", headers=headers, timeout=DEFAULT_TIMEOUT)
        if resp.status_code == 404:
            raise UserNotFoundError(f"GitHub user '{username}' not found")
        resp.raise_for_status()
        profile = resp.json()

        total_stars = 0
        page = 1
        while True:
            repos_resp = session.get(
                f"https://api.github.com/users/{username}/repos",
                headers=headers,
                params={"per_page": 100, "page": page, "sort": "stars"},
                timeout=DEFAULT_TIMEOUT,
            )
            repos_resp.raise_for_status()
            repos = repos_resp.json()
            if not repos:
                break
            total_stars += sum(r.get("stargazers_count", 0) for r in repos)
            if len(repos) < 100:
                break
            page += 1

        return {
            "public_repos": profile.get("public_repos", 0),
            "followers": profile.get("followers", 0),
            "total_stars": total_stars,
            "avatar_url": profile.get("avatar_url", ""),
            "name": profile.get("name", username),
        }

    def compute_scores(self, data: dict) -> dict:
        metrics = {
            "stars": self._metric(data.get("total_stars", 0), self._stars_pct),
            "repos": self._metric(data.get("public_repos", 0), self._repos_pct),
            "followers": self._metric(data.get("followers", 0), self._followers_pct),
        }

        avg_percentile = sum(v["percentile"] for v in metrics.values()) / len(metrics)
        return {"power_score": int(avg_percentile * 10), "metrics": metrics}

    def _metric(self, value: int, pct_fn) -> dict:
        return {"value": value, "percentile": pct_fn(value)}

    def _stars_pct(self, stars: int) -> float:
        if stars == 0:
            return 10.0
        return min(50 + 15 * math.log10(max(stars, 1)) * 2, 99.9)

    def _repos_pct(self, repos: int) -> float:
        if repos == 0:
            return 10.0
        return min(40 + 12 * math.log10(max(repos, 1)) * 2, 99.0)

    def _followers_pct(self, followers: int) -> float:
        if followers == 0:
            return 15.0
        return min(50 + 14 * math.log10(max(followers, 1)) * 2, 99.9)


register(GitHubAdapter())

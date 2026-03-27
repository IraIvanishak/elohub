"""Base platform adapter — the contract every platform must implement."""

from abc import ABC, abstractmethod

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()
session.headers.update({"User-Agent": "SkillBoard/1.0 (contact: skillboard@example.com)"})
retry = Retry(total=2, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
session.mount("https://", HTTPAdapter(max_retries=retry))

DEFAULT_TIMEOUT = 20


class PlatformError(Exception):
    pass


class UserNotFoundError(PlatformError):
    pass


class PlatformAdapter(ABC):
    """Every platform adapter must define slug, label, fetch(), and compute_scores()."""

    slug: str   # DB key, e.g. "chess_com"
    label: str  # UI label, e.g. "Chess.com"

    @abstractmethod
    def fetch(self, username: str, **kwargs) -> dict:
        """Hit external API and return raw data dict.

        Raises UserNotFoundError if username doesn't exist.
        Raises PlatformError on other failures.
        """

    @abstractmethod
    def compute_scores(self, data: dict) -> dict:
        """Convert raw data into {"power_score": int, "metrics": {key: {"value": x, "percentile": y}}}."""

"""Platform registry — auto-discovers adapters and provides a simple public API."""

from .base import PlatformAdapter, PlatformError, UserNotFoundError

_REGISTRY: dict[str, PlatformAdapter] = {}


def register(adapter: PlatformAdapter):
    _REGISTRY[adapter.slug] = adapter


def get_adapter(slug: str) -> PlatformAdapter:
    if slug not in _REGISTRY:
        raise PlatformError(f"Unknown platform: {slug}")
    return _REGISTRY[slug]


def all_adapters() -> dict[str, PlatformAdapter]:
    return dict(_REGISTRY)


def platform_labels() -> dict[str, str]:
    return {slug: a.label for slug, a in _REGISTRY.items()}


# Import adapters to trigger registration
from . import chess_com, github  # noqa: E402, F401

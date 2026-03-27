"""Profile and platform account management."""

from __future__ import annotations

from datetime import datetime, timezone

from app import db
from app.models import PlatformAccount, User
from app.platforms import UserNotFoundError, get_adapter, platform_labels


class PlatformAlreadyConnected(Exception):
    pass


def get_user_by_username(username: str) -> User | None:
    return User.query.filter_by(username=username).first()


def connect_platform(user: User, platform: str, platform_username: str, token: str | None = None) -> PlatformAccount:
    """Validate username on platform, fetch data, compute scores, save.

    Raises:
        PlatformAlreadyConnected: if user already has this platform
        UserNotFoundError: if username doesn't exist on platform
        Exception: on API errors
    """
    labels = platform_labels()
    if PlatformAccount.query.filter_by(user_id=user.id, platform=platform).first():
        raise PlatformAlreadyConnected(f"{labels.get(platform, platform)} already connected.")

    adapter = get_adapter(platform)
    data = adapter.fetch(platform_username, token=token)
    scores = adapter.compute_scores(data)

    account = PlatformAccount(
        user_id=user.id,
        platform=platform,
        platform_username=platform_username,
        cached_data=data,
        cached_at=datetime.now(timezone.utc),
        scores=scores,
    )
    db.session.add(account)
    db.session.commit()
    return account


def disconnect_platform(user: User, account_id: int) -> bool:
    """Remove a platform account. Returns False if not owned by user."""
    account = db.session.get(PlatformAccount, account_id)
    if not account or account.user_id != user.id:
        return False
    db.session.delete(account)
    db.session.commit()
    return True


def refresh_all(user: User, token: str | None = None) -> list[str]:
    """Refresh data for all connected platforms. Returns list of error messages."""
    labels = platform_labels()
    errors = []
    for account in user.platforms:
        try:
            adapter = get_adapter(account.platform)
            t = token if account.platform == "github" else None
            data = adapter.fetch(account.platform_username, token=t)
            account.cached_data = data
            account.cached_at = datetime.now(timezone.utc)
            account.scores = adapter.compute_scores(data)
        except Exception:
            errors.append(f"Could not refresh {labels.get(account.platform, account.platform)}.")
    db.session.commit()
    return errors

"""Seed in-memory DB with example users."""

from datetime import datetime, timezone

from app import db
from app.models import PlatformAccount, User
from app.platforms import get_adapter


def seed_data():
    u1 = User(email="maksym@example.com", username="maksym")
    u1.set_password("password")

    u2 = User(email="anya@example.com", username="anya")
    u2.set_password("password")

    u3 = User(email="oleh@example.com", username="oleh")
    u3.set_password("password")

    db.session.add_all([u1, u2, u3])
    db.session.flush()
    now = datetime.now(timezone.utc)

    chess = get_adapter("chess_com")
    github = get_adapter("github")

    seed_accounts = [
        # Maksym: strong chess, moderate GitHub
        (u1, chess, "maxchess97", {"rapid_rating": 1400, "blitz_rating": 1250, "bullet_rating": 1100, "puzzle_rating": 1800}),
        (u1, github, "maxdev97", {"public_repos": 12, "followers": 8, "total_stars": 45, "avatar_url": "", "name": "Maksym"}),
        # Anya: moderate chess, strong GitHub
        (u2, chess, "anya_chess", {"rapid_rating": 1150, "blitz_rating": 1050, "bullet_rating": 900, "puzzle_rating": 1500}),
        (u2, github, "anya-dev", {"public_repos": 35, "followers": 120, "total_stars": 320, "avatar_url": "", "name": "Anya"}),
        # Oleh: GitHub only, very strong
        (u3, github, "oleh-oss", {"public_repos": 58, "followers": 450, "total_stars": 520, "avatar_url": "", "name": "Oleh"}),
    ]

    for user, adapter, username, data in seed_accounts:
        account = PlatformAccount(
            user_id=user.id,
            platform=adapter.slug,
            platform_username=username,
            cached_data=data,
            cached_at=now,
            scores=adapter.compute_scores(data),
        )
        db.session.add(account)

    db.session.commit()

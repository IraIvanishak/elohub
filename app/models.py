from datetime import datetime, timezone

import bcrypt
from flask_login import UserMixin

from app import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    display_name = db.Column(db.String(120), nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    platforms = db.relationship("PlatformAccount", backref="user", lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def check_password(self, password):
        return bcrypt.checkpw(password.encode(), self.password_hash.encode())

    @property
    def power_score(self):
        scores = [p.scores for p in self.platforms if p.scores]
        if not scores:
            return 0
        return int(sum(s["power_score"] for s in scores) / len(scores))

    @property
    def league(self):
        return get_league(self.power_score)

    def platform_dict(self):
        return {p.platform: p for p in self.platforms}


class PlatformAccount(db.Model):
    __tablename__ = "platform_accounts"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    platform = db.Column(db.String(50), nullable=False)
    platform_username = db.Column(db.String(255), nullable=False)
    cached_data = db.Column(db.JSON, nullable=True)
    cached_at = db.Column(db.DateTime, nullable=True)
    scores = db.Column(db.JSON, nullable=True)

    __table_args__ = (db.UniqueConstraint("user_id", "platform"),)

    @property
    def is_cache_fresh(self):
        if not self.cached_at:
            return False
        from config import Config
        age = (datetime.now(timezone.utc) - self.cached_at).total_seconds()
        return age < Config.CACHE_TTL_SECONDS


LEAGUES = [
    (0, "Unranked", "#6b7280"),
    (200, "Bronze", "#cd7f32"),
    (350, "Silver", "#c0c0c0"),
    (500, "Gold", "#ffd700"),
    (650, "Platinum", "#00d4aa"),
    (800, "Diamond", "#b9f2ff"),
    (950, "Legend", "#ff4500"),
]


def get_league(power_score):
    name, color = "Unranked", "#6b7280"
    for threshold, league_name, league_color in LEAGUES:
        if power_score >= threshold:
            name, color = league_name, league_color
    return {"name": name, "color": color, "score": power_score}

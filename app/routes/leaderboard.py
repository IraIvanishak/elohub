from flask import Blueprint, render_template

from app.models import User

leaderboard_bp = Blueprint("leaderboard", __name__)


@leaderboard_bp.route("/")
def index():
    users = User.query.all()
    users.sort(key=lambda u: u.power_score, reverse=True)
    return render_template("index.html", users=users)

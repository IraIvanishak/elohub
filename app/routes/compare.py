from flask import Blueprint, render_template, request

from app.platforms import platform_labels
from app.models import User
from app.services.compare_service import build_comparison
from app.services.profile_service import get_user_by_username

compare_bp = Blueprint("compare", __name__)


@compare_bp.route("/compare")
def compare_select():
    users = User.query.order_by(User.username).all()
    user1_name = request.args.get("user1", "")
    user2_name = request.args.get("user2", "")

    if not user1_name or not user2_name:
        return render_template("compare_select.html", users=users, result=None)

    user1 = get_user_by_username(user1_name)
    user2 = get_user_by_username(user2_name)

    if not user1 or not user2:
        return render_template("compare_select.html", users=users, result=None, error="User not found.")

    result = build_comparison(user1, user2)
    return render_template("compare.html", user1=user1, user2=user2, result=result, platform_labels=platform_labels())


@compare_bp.route("/compare/<username1>/<username2>")
def compare_users(username1, username2):
    user1 = get_user_by_username(username1)
    user2 = get_user_by_username(username2)
    if not user1 or not user2:
        return "User not found", 404
    result = build_comparison(user1, user2)
    return render_template("compare.html", user1=user1, user2=user2, result=result, platform_labels=platform_labels())

from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.platforms import UserNotFoundError, platform_labels
from app.services.profile_service import (
    PlatformAlreadyConnected,
    connect_platform,
    disconnect_platform,
    get_user_by_username,
    refresh_all,
)

profile_bp = Blueprint("profile", __name__)


@profile_bp.route("/profile")
@login_required
def my_profile():
    return render_template("profile.html", user=current_user, is_own=True, platform_labels=platform_labels())


@profile_bp.route("/u/<username>")
def public_profile(username):
    user = get_user_by_username(username)
    if not user:
        return "User not found", 404
    return render_template("profile.html", user=user, is_own=False, platform_labels=platform_labels())


@profile_bp.route("/profile/add-platform", methods=["POST"])
@login_required
def add_platform():
    platform = request.form.get("platform", "").strip()
    platform_username = request.form.get("platform_username", "").strip()
    labels = platform_labels()

    if platform not in labels:
        flash("Invalid platform.", "error")
        return redirect(url_for("profile.my_profile"))

    if not platform_username:
        flash("Username is required.", "error")
        return redirect(url_for("profile.my_profile"))

    try:
        token = current_app.config.get("GITHUB_TOKEN") if platform == "github" else None
        connect_platform(current_user, platform, platform_username, token=token)
        flash(f"{labels[platform]} connected!", "success")
    except PlatformAlreadyConnected as e:
        flash(str(e), "error")
    except UserNotFoundError as e:
        flash(str(e), "error")
    except Exception:
        flash(f"Could not reach {labels[platform]}. Try again later.", "error")

    return redirect(url_for("profile.my_profile"))


@profile_bp.route("/profile/remove-platform/<int:account_id>", methods=["POST"])
@login_required
def remove_platform(account_id):
    if disconnect_platform(current_user, account_id):
        flash("Platform removed.", "success")
    else:
        flash("Not authorized.", "error")
    return redirect(url_for("profile.my_profile"))


@profile_bp.route("/profile/refresh", methods=["POST"])
@login_required
def refresh_data():
    token = current_app.config.get("GITHUB_TOKEN")
    errors = refresh_all(current_user, token=token)
    for err in errors:
        flash(err, "error")
    if not errors:
        flash("Data refreshed!", "success")
    return redirect(url_for("profile.my_profile"))

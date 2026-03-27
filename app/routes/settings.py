"""User settings routes."""

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import db

settings_bp = Blueprint("settings", __name__)


@settings_bp.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    if request.method == "POST":
        display_name = request.form.get("display_name", "").strip()
        current_user.display_name = display_name or None
        db.session.commit()
        flash("Settings saved.", "success")
        return redirect(url_for("settings.settings"))

    return render_template("settings.html")

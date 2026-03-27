from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

from app.services.user_service import UserExistsError, authenticate, register_user

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not email or not username or not password:
            flash("All fields are required.", "error")
            return render_template("auth/register.html")

        try:
            user = register_user(email, username, password)
        except UserExistsError as e:
            flash(f"{e.field.title()} already taken.", "error")
            return render_template("auth/register.html")

        login_user(user)
        return redirect(url_for("profile.my_profile"))

    return render_template("auth/register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = authenticate(
            request.form.get("email", "").strip(),
            request.form.get("password", ""),
        )
        if user:
            login_user(user)
            return redirect(request.args.get("next") or url_for("profile.my_profile"))
        flash("Invalid email or password.", "error")

    return render_template("auth/login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))

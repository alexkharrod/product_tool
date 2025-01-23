from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from application import db
from application.forms import LoginForm
from application.models.user import User

bp = Blueprint("auth", __name__)


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.get_by_email(form.email.data)

        if user is None or not user.check_password(form.password.data):
            flash("Invalid email or password", "danger")
            return redirect(url_for("auth.login"))

        login_user(user, remember=form.remember.data)
        flash(f"Welcome back {user.email}!", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template("auth/login.html", form=form)


@bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if request.method == "POST":
        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")

        if not current_user.check_password(current_password):
            flash("Current password is incorrect", "danger")
            return redirect(url_for("auth.profile"))

        if new_password != confirm_password:
            flash("New passwords do not match", "danger")
            return redirect(url_for("auth.profile"))

        if len(new_password) < 8:
            flash("Password must be at least 8 characters", "danger")
            return redirect(url_for("auth.profile"))

        current_user.set_password(new_password)
        db.session.commit()
        flash("Password updated successfully", "success")
        return redirect(url_for("auth.profile"))

    return render_template("auth/profile.html")


@bp.route("/logout", methods=["POST"])
@login_required
def logout():
    """Log out current user and clear session cookies"""
    if not current_user.is_authenticated:
        flash("You were not logged in", "warning")
        return redirect(url_for("auth.login"))

    logout_user()
    flash("You have been logged out", "success")
    return redirect(url_for("auth.login"))

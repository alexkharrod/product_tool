from datetime import datetime, timedelta

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required, login_user, logout_user

from application import db
from application.forms import LoginForm
from application.models.user import Permission, User

bp = Blueprint("auth", __name__)


@bp.route("/login", methods=["GET", "POST"])
def login():
    try:
        if current_user.is_authenticated:
            return redirect(url_for("main.index"))

        form = LoginForm()

        if form.validate_on_submit():
            user = User.get_by_email(form.email.data)

            # Security: Prevent user enumeration
            if not user or not user.check_password(form.password.data):
                current_app.logger.warning(
                    f"Failed login attempt for email: {form.email.data}"
                )
                flash("Invalid credentials", "danger")
                return redirect(url_for("auth.login"))

            # Security: Check account status
            if not user.active:
                flash("This account is deactivated", "danger")
                return redirect(url_for("auth.login"))

            # Security: Check failed attempts and lock duration
            if user.failed_attempts >= 5:
                if user.locked_until and user.locked_until > datetime.utcnow():
                    flash("Account locked - contact support", "danger")
                    return redirect(url_for("auth.login"))
                # Auto-unlock after 1 hour
                user.locked_until = datetime.utcnow() + timedelta(hours=1)
                db.session.commit()
                flash("Account locked - contact support", "danger")
                return redirect(url_for("auth.login"))

            login_user(user, remember=form.remember.data)
            user.failed_login_attempts = 0  # Reset counter
            db.session.commit()

            # Audit logging
            current_app.logger.info(f"User login: {user.id}")

            # Role-based redirect
            redirect_to = (
                url_for("admin.dashboard")
                if user.permissions & Permission.ADMIN
                else url_for("main.index")
            )
            return redirect(redirect_to)

        return render_template("auth/login.html", form=form)

    except Exception as e:
        current_app.logger.error(f"Login error: {str(e)}", exc_info=True)
        flash("Authentication service unavailable - try again later", "danger")
        return redirect(url_for("auth.login"))


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

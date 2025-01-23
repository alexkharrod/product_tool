from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user
from application.models.user import User
from application.forms import LoginForm

bp = Blueprint("auth", __name__)

@bp.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
        
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.get_by_email(form.email.data)
        
        if user is None or not user.check_password(form.password.data):
            flash("Invalid email or password", "danger")
            return redirect(url_for('auth.login'))
            
        login_user(user, remember=form.remember.data)
        flash(f"Welcome back {user.email}!", "success")
        return redirect(url_for('main.dashboard'))
        
    return render_template("auth/login.html", form=form)

@bp.route("/logout", methods=["POST"])
def logout():
    """Log out current user and clear session cookies"""
    if not current_user.is_authenticated:
        flash("You were not logged in", "warning")
        return redirect(url_for('auth.login'))
        
    logout_user()
    flash("You have been logged out", "success")
    return redirect(url_for('auth.login'))

from flask import Blueprint, render_template, redirect, url_for
from application.forms import LoginForm

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Handle login logic
        return redirect(url_for('main.index'))
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
def logout():
    # Handle logout logic
    return redirect(url_for('main.index'))

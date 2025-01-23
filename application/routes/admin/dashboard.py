from flask import render_template, abort
from flask_login import current_user, login_required
from application import db
from application.models import Quote, Product, User
from flask import Blueprint

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.before_request
@login_required
def restrict_admin_access():
    if not current_user.is_admin():
        abort(403)

@admin_bp.route('', strict_slashes=False)
@admin_bp.route('/', strict_slashes=False)
def dashboard():
    stats = {
        'open_quotes': Quote.query.filter_by(status='open').count(),
        'recent_quotes': Quote.query.order_by(Quote.created_at.desc()).limit(5).all(),
        'pending_products': Product.query.filter_by(completion_status=False).count(),
        'user_activity': User.query.order_by(User.last_login.desc()).limit(5).all()
    }
    return render_template('admin/dashboard.html', stats=stats)

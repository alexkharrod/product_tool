from flask import render_template, abort, redirect, url_for, flash
from flask_login import current_user, login_required
from application import db
from application.models import User, Product, Quote
from application.forms import CreateUserForm, EditUserForm
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
        'total_users': User.query.count(),
        'total_products': Product.query.count(),
        'open_quotes': Quote.query.filter_by(status='open').count(),
        'pending_products': Product.query.filter_by(completion_status=False).count(),
        'recent_users': User.query.order_by(User.last_login.desc()).limit(5).all()
    }
    return render_template('admin/dashboard.html', stats=stats)

@admin_bp.route('/users')
def users():
    all_users = User.query.order_by(User.email).all()
    return render_template('admin/users.html', users=all_users)

@admin_bp.route('/edit-user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = EditUserForm(obj=user)
    
    if form.validate_on_submit():
        user.email = form.email.data
        user.role = form.role.data
        
        if form.password.data:
            user.set_password(form.password.data)
            
        db.session.commit()
        flash('User updated successfully', 'success')
        return redirect(url_for('admin.users'))
    
    return render_template('admin/edit_user.html', form=form, user=user)

@admin_bp.route('/add-user', methods=['GET', 'POST'])
def add_user():
    form = CreateUserForm()
    if form.validate_on_submit():
        user = User(
            email=form.email.data,
            role=form.role.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('User created successfully', 'success')
        return redirect(url_for('admin.users'))
    return render_template('admin/add_user.html', form=form)

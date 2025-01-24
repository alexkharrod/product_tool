from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from application import db
from application.models.product import Product
from application.forms import ProductSearchForm, ProductForm

product = Blueprint('product', __name__)

@product.route('/products')
def list():
    products = Product.query.all()
    search_form = ProductSearchForm()
    create_form = ProductForm()
    return render_template('products/product.html', 
                         products=products,
                         search_form=search_form,
                         create_form=create_form)

@product.route('/products/create', methods=['GET', 'POST'])
@login_required
def create():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            description=form.description.data,
            created_by=current_user.id
        )
        db.session.add(product)
        db.session.commit()
        flash('Product created successfully', 'success')
        return redirect(url_for('product.list'))
    return render_template('products/product.html', create_form=form)

@product.route('/products/search', methods=['GET', 'POST'])
def search():
    form = ProductSearchForm()
    if form.validate_on_submit():
        query = Product.query
        if form.sku.data:
            query = query.filter(Product.sku.ilike(f"%{form.sku.data}%"))
        if form.vendor_name.data:
            query = query.filter(Product.vendor.ilike(f"%{form.vendor_name.data}%"))
        products = query.all()
        return render_template('products/product.html',
                             products=products,
                             search_form=form)
    return render_template('products/product.html', search_form=form)

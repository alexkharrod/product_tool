from flask import Blueprint, render_template, redirect, url_for, flash
from application import db
from application.models.product import Product
from application.forms import ProductForm


product = Blueprint('product', __name__)

@product.route('/products')
def list_products():
    products = Product.query.all()
    return render_template('products/products.html', products=products)

@product.route('/product/create', methods=['GET', 'POST'])
def create():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product()
        form.populate_obj(product)
        db.session.add(product)
        db.session.commit()
        flash('Product created successfully!', 'success')
        return redirect(url_for('product.list_products'))
    return render_template('products/create.html', form=form)

@product.route('/product/view/<int:id>')
def view(id):
    product = Product.query.get_or_404(id)
    return render_template('products/view.html', product=product)

@product.route('/product/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    product = Product.query.get_or_404(id)
    form = ProductForm(obj=product)
    if form.validate_on_submit():
        form.populate_obj(product)
        db.session.commit()
        flash('Product updated successfully', 'success')
        return redirect(url_for('product.view', id=product.id))
    return render_template('products/edit.html', form=form, product=product)

@product.route('/product/delete/<int:id>', methods=['POST'])
def delete(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully', 'success')
    return redirect(url_for('product.list_products'))

from flask import Blueprint, render_template, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
import traceback
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
        try:
            current_app.logger.debug(f"Form data: {form.data}")
            
            product = Product(
                sku=form.sku.data.strip(),
                name=form.name.data.strip(),
                vendor_name=form.vendor_name.data.strip(),
                vendor_part_number=form.vendor_part_number.data.strip(),
                category=form.category.data.strip(),
                image_url=form.image_url.data.strip(),
                description=form.description.data.strip(),
                length=form.length.data,
                width=form.width.data,
                height=form.height.data,
                weight=form.weight.data,
                quantity_per_ctn=form.quantity_per_ctn.data,
                moq=form.moq.data,
                package_type=form.package_type.data.strip(),
                production_time=form.production_time.data.strip(),
                imprint_location=form.imprint_location.data.strip(),
                imprint_dimensions=form.imprint_dimensions.data.strip(),
                imprint_types=form.imprint_types.data.strip(),
                keywords=form.keywords.data.strip(),
                created_by=current_user
            )

            db.session.add(product)
            db.session.commit()
            
            flash(f'Successfully created product: {product.sku}', 'success')
            current_app.logger.info(f"Created product {product.id} - {product.sku}")
            return redirect(url_for('product.list'))

        except Exception as e:
            db.session.rollback()
            error_msg = f"Failed to create product: {str(e)}"
            current_app.logger.error(f"{error_msg}\n{traceback.format_exc()}")
            flash(error_msg, 'danger')
    else:
        # Log form validation errors
        if form.errors:
            current_app.logger.warning(f"Form validation errors: {form.errors}")
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"{getattr(form, field).label.text}: {error}", 'warning')

    return render_template('products/product.html',
                         products=Product.query.all(),
                         search_form=ProductSearchForm(),
                         create_form=form)

@product.route('/products/search', methods=['GET', 'POST'])
def search():
    form = ProductSearchForm()
    if form.validate_on_submit():
        query = Product.query
        if form.sku.data:
            query = query.filter(Product.sku.ilike(f"%{form.sku.data}%"))
        if form.vendor_name.data:
            query = query.filter(Product.vendor_name.ilike(f"%{form.vendor_name.data}%"))
            
        return render_template('products/product.html',
                             products=query.all(),
                             search_form=form)
                             
    return render_template('products/product.html', search_form=form)

from flask import Blueprint, render_template

bp = Blueprint('product', __name__)

@bp.route('/products')
def product_list():
    return render_template('products/product.html')

from flask import Blueprint, render_template

bp = Blueprint('quote', __name__)

@bp.route('/quotes')
def quote_list():
    return render_template('products/quote.html')

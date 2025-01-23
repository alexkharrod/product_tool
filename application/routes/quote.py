import logging
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from application.models.quote import Quote
from application.forms import QuoteForm
from application import db

bp = Blueprint('quote', __name__)

@bp.route('/quotes')
@login_required
def quote_list():
    quotes = Quote.query.filter_by(user_id=current_user.id).all()
    return render_template('quotes/list.html', quotes=quotes)

@bp.route('/quotes/create', methods=['GET', 'POST'])
@login_required
def create_quote():
    """Handle quote creation with validation and error logging"""
    form = QuoteForm()
    if form.validate_on_submit():
        try:
            quote = Quote(
                title=form.title.data.strip(),
                content=form.content.data.strip(),
                user_id=current_user.id
            )
            db.session.add(quote)
            db.session.commit()
            flash('Quote created successfully', 'success')
            return redirect(url_for('quote.quote_list'))
        except ValueError as ve:
            db.session.rollback()
            logging.error(f'Validation error creating quote: {str(ve)}')
            flash(f'Invalid data: {str(ve)}', 'danger')
        except Exception as e:
            db.session.rollback()
            logging.error(f'Error creating quote: {str(e)}', exc_info=True)
            flash('Failed to create quote. Please try again.', 'danger')
    return render_template('quotes/create.html', form=form)

@bp.route('/quotes/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_quote(id):
    """Handle quote updates with proper authorization and error handling"""
    quote = Quote.query.get_or_404(id)
    
    # Verify ownership or admin access
    if quote.user_id != current_user.id and not current_user.is_admin:
        logging.warning(f'Unauthorized edit attempt by user {current_user.id} on quote {id}')
        flash('You are not authorized to edit this quote', 'danger')
        return redirect(url_for('quote.quote_list'))
    
    form = QuoteForm(obj=quote)
    if form.validate_on_submit():
        try:
            form.populate_obj(quote)
            quote.title = form.title.data.strip()
            quote.content = form.content.data.strip()
            db.session.commit()
            flash('Quote updated successfully', 'success')
            return redirect(url_for('quote.quote_list'))
        except ValueError as ve:
            db.session.rollback()
            logging.error(f'Validation error updating quote {id}: {str(ve)}')
            flash(f'Invalid data: {str(ve)}', 'danger')
        except Exception as e:
            db.session.rollback()
            logging.error(f'Error updating quote {id}: {str(e)}', exc_info=True)
            flash('Failed to update quote. Please try again.', 'danger')
    return render_template('quotes/edit.html', form=form, quote=quote)

import logging
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError
from application.models.quote import Quote, QuoteTier
from application.models.product import Product
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
    """Handle quote creation with product selection and tiered pricing"""
    form = QuoteForm()
    form.product_sku.choices = [(p.sku, p.name) for p in Product.query.all()]
    
    if form.add_tier.data:
        form.tiers.append_entry()
        return render_template('quotes/create.html', form=form)
        
    if form.validate_on_submit():
        try:
            # Get selected product
            product = Product.query.filter_by(sku=form.product_sku.data).first()
            if not product:
                flash('Selected product not found', 'danger')
                return redirect(url_for('quote.create_quote'))
            
            # Create new quote
            quote = Quote(
                customer_name=form.customer_name.data.strip(),
                user_id=current_user.id,
                product_sku=product.sku,
                length=form.length.data,
                width=form.width.data,
                height=form.height.data,
                weight=form.weight.data,
                quantity_per_ctn=form.quantity_per_ctn.data,
                status='Draft',
                quote_number=Quote.generate_quote_number()
            )
            db.session.add(quote)
            db.session.flush()
            
            # Process tiers with validation
            for idx, tier_form in enumerate(form.tiers):
                # Create and validate tier
                tier = QuoteTier(
                    tier_number=idx+1,
                    quantity=int(tier_form.quantity.data),
                    quote_price=float(tier_form.quote_price.data),
                    air_freight=float(tier_form.air_freight.data or 0.0),
                    ocean_freight=float(tier_form.ocean_freight.data or 0.0),
                    markup=float(tier_form.markup.data or 0.0),
                    product_sku=product.sku
                )
                
                if tier.quantity < 1:
                    raise ValueError(f"Tier {idx+1} quantity must be at least 1")
                
                # Add tier through relationship
                quote.tiers.append(tier)
            
            # Validate quantity progression
            tiers = sorted(quote.tiers, key=lambda t: t.quantity)
            prev_qty = 0
            for i, tier in enumerate(tiers):
                if i == 0 and tier.quantity < 1:
                    raise ValueError("First tier quantity must be at least 1")
                if i > 0 and tier.quantity <= prev_qty:
                    raise ValueError(f"Tier {i+1} quantity must be greater than previous")
                prev_qty = tier.quantity
            
            db.session.commit()
            flash('Quote with tiers saved successfully', 'success')
            return redirect(url_for('quote.quote_list'))
        except ValueError as ve:
            db.session.rollback()
            logging.error(f'Validation error creating quote: {str(ve)}')
            flash(f'Invalid data: {str(ve)}', 'danger')
        except IntegrityError as ie:
            db.session.rollback()
            logging.error(f'Database integrity error: {str(ie)}')
            flash('A product with this SKU already exists. Please use a unique SKU.', 'danger')
        except Exception as e:
            db.session.rollback()
            logging.error(f'Error creating quote: {str(e)}', exc_info=True)
            flash(f'Failed to create quote: {str(e)}', 'danger')
    return render_template('quotes/create.html', form=form)

@bp.route('/quotes/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_quote(id):
    """Handle quote updates with dynamic tiers"""
    quote = Quote.query.get_or_404(id)
    
    # Verify ownership or admin access
    if quote.user_id != current_user.id and not current_user.is_admin:
        logging.warning(f'Unauthorized edit attempt by user {current_user.id} on quote {id}')
        flash('You are not authorized to edit this quote', 'danger')
        return redirect(url_for('quote.quote_list'))
    
    form = QuoteForm(obj=quote)
    
    # Handle "Add Tier" button click
    if form.add_tier.data:
        form.tiers.append_entry()
        return render_template('quotes/edit.html', form=form, quote=quote)
    
    # Populate existing tiers
    if not form.tiers.entries:
        for tier in quote.tiers:
            tier_form = form.tiers.append_entry()
            tier_form.quantity.data = tier.quantity
            tier_form.quote_price.data = tier.quote_price
            tier_form.air_freight.data = tier.air_freight
            tier_form.ocean_freight.data = tier.ocean_freight
            tier_form.markup.data = tier.markup
    
    if form.validate_on_submit():
        try:
            with db.session.begin_nested():
                # Update base fields
                quote.customer_name = form.customer_name.data.strip()
                
                # Clear existing tiers
                quote.tiers = []
                
                # Process tiers through WTForms
                for idx, tier_form in enumerate(form.tiers):
                    tier = QuoteTier(
                        tier_number=idx+1,
                        quantity=tier_form.quantity.data,
                        quote_price=tier_form.quote_price.data,
                        air_freight=tier_form.air_freight.data or 0.0,
                        ocean_freight=tier_form.ocean_freight.data or 0.0,
                        markup=tier_form.markup.data or 0.0
                    )
                    quote.tiers.append(tier)
                
                # Validate quantity progression
                tiers = sorted(quote.tiers, key=lambda t: t.quantity)
                prev_qty = 0
                for i, tier in enumerate(tiers):
                    if i == 0 and tier.quantity < 1:
                        raise ValueError("First tier quantity must be at least 1")
                    if i > 0 and tier.quantity <= prev_qty:
                        raise ValueError(f"Tier {i+1} quantity must be greater than previous")
                    prev_qty = tier.quantity
            
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

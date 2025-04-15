from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models.inventory import Inventory
from models.sales import Sale
from models.restock import Restock
from models.history import History
from datetime import datetime
from . import dashboard_bp
from utils.forecast_service import generate_stock_forecast

@dashboard_bp.before_request
def run_forecasting():
    generate_stock_forecast()

@dashboard_bp.route('/dashboard')
@login_required
def view():
    inventory_items = Inventory.query.all()

    total_products = len(inventory_items)
    healthy_stock = sum(1 for item in inventory_items if item.stock_level > item.min_threshold * 1.5)
    near_min_stock = sum(1 for item in inventory_items if item.stock_level <= item.min_threshold * 1.5 and item.stock_level > item.min_threshold)
    low_stock = sum(1 for item in inventory_items if item.stock_level <= item.min_threshold and item.stock_level > 0)
    out_of_stock = sum(1 for item in inventory_items if item.stock_level == 0)

    return render_template(
        'dashboard.html',
        inventory=inventory_items,
        total_products=total_products,
        healthy_stock=healthy_stock,
        near_min_stock=near_min_stock,
        low_stock=low_stock,
        out_of_stock=out_of_stock
    )

@dashboard_bp.route('/dashboard/add_stock/<int:item_id>', methods=['POST'])
@login_required
def add_stock(item_id):
    item = Inventory.query.get_or_404(item_id)
    try:
        added_stock = int(request.form.get('stock_value', 0))
        if added_stock > 0:
            item.stock_level += added_stock
            
            # Create a Restock entry
            restock_entry = Restock(
                inventory_id=item.id,
                quantity_added=added_stock,
                cost_price_at_time=item.cost_price,
                total_cost=item.cost_price * added_stock,
                restocked_at=datetime.utcnow()
            )
            db.session.add(restock_entry)

            # Log the action in History
            history_entry = History(
                user_id=current_user.id,
                inventory_id=item.id,
                action_type="add_stock",
                description=f"added {item.name} stocks by {added_stock} {item.unit_type.name.lower()}s",
                timestamp=datetime.utcnow()
            )
            db.session.add(history_entry)

            db.session.commit()
            flash(f"Stock increased by {added_stock} for {item.name}.", "success")
        else:
            flash("Invalid stock value!", "danger")
    except ValueError:
        flash("Invalid input! Please enter a number.", "danger")

    return redirect(url_for('dashboard.view'))

@dashboard_bp.route('/dashboard/remove_stock/<int:item_id>', methods=['POST'])
@login_required
def remove_stock(item_id):
    item = Inventory.query.get_or_404(item_id)
    try:
        removed_stock = int(request.form.get('stock_value', 0))
        if removed_stock > 0:
            if item.stock_level >= removed_stock:
                item.stock_level -= removed_stock
                
                # Create a Sales entry
                sales_entry = Sale(
                    inventory_id=item.id,
                    quantity_sold=removed_stock,
                    selling_price_at_time=item.selling_price,
                    total_revenue=item.selling_price * removed_stock,
                    sold_at=datetime.utcnow()
                )
                db.session.add(sales_entry)

                # Log the action in History
                history_entry = History(
                    user_id=current_user.id,
                    inventory_id=item.id,
                    action_type="remove_stock",
                    description=f"reduced {item.name} stocks by {removed_stock} {item.unit_type.name.lower()}s",
                    timestamp=datetime.utcnow()
                )
                db.session.add(history_entry)

                db.session.commit()
                flash(f"Stock decreased by {removed_stock} for {item.name}.", "warning")
            else:
                flash(f"Cannot remove {removed_stock} stocks. Only {item.stock_level} available.", "danger")
        else:
            flash("Invalid stock value!", "danger")
    except ValueError:
        flash("Invalid input! Please enter a number.", "danger")

    return redirect(url_for('dashboard.view'))

import datetime
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user
from extensions import db
from models.sales import Sale
from models.notification import Notification
from . import sales_bp

@sales_bp.route('/sales')
@login_required
def view():
    recent_sales = Sale.query.order_by(Sale.sold_at.desc()).limit(50).all()

    return render_template(
        'sales.html', 
        sales=recent_sales
    )

@sales_bp.route('/sales/delete/<int:sale_id>', methods=['POST'])
@login_required
def delete_sale(sale_id):
    sale = Sale.query.get(sale_id)
    inventory_name = sale.inventory.name if sale.inventory else "Unknown Item"

    if not sale:
        flash("Sale record not found.", "danger")
        return redirect(url_for('sales.view'))

    try:
        db.session.delete(sale)
        db.session.commit()

        flash("Sale record deleted successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash("An error occurred while deleting the sale.", "danger")

    return redirect(url_for('sales.view'))
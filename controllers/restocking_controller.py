import datetime
from flask import render_template, flash, redirect, url_for, request, Blueprint
from flask_login import login_required, current_user
from extensions import db
from models.restock import Restock
from models.notification import Notification
from . import restocking_bp

restocking_bp = Blueprint('restocking', __name__)

@restocking_bp.route('/restocking')
@login_required
def view():
    recent_restock = Restock.query.order_by(Restock.restocked_at.desc()).limit(50).all()

    return render_template(
        'restocking.html',
        restocks=recent_restock
    )

@restocking_bp.route('/restocks/delete/<int:restock_id>', methods=['POST'])
@login_required
def delete_restock(restock_id):
    restock = Restock.query.get(restock_id)
    inventory_name = restock.inventory.name if restock.inventory else "Unknown Item"
    db.session.delete(restock)
    db.session.commit()

    flash("Restock record deleted successfully!", "danger")
    return redirect(url_for('restocking.view'))

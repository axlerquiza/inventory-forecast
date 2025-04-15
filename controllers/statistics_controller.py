from flask import Blueprint, render_template, jsonify
from flask_login import login_required
from extensions import db
from models.inventory import Inventory
from models.sales import Sale
from models.restock import Restock
from sqlalchemy.sql import func

statistics_bp = Blueprint('statistics', __name__)

@statistics_bp.route('/statistics')
@login_required
def view():
    inventory_items = Inventory.query.all()
    total_products = len(inventory_items)
    healthy_stock = sum(1 for item in inventory_items if item.stock_level > item.min_threshold * 1.5)
    near_min_stock = sum(1 for item in inventory_items if item.stock_level <= item.min_threshold * 1.5 and item.stock_level > item.min_threshold)
    low_stock = sum(1 for item in inventory_items if item.stock_level <= item.min_threshold and item.stock_level > 0)
    out_of_stock = sum(1 for item in inventory_items if item.stock_level == 0)
    
    total_revenue = db.session.query(func.sum(Sale.total_revenue)).scalar() or 0
    total_purchases = db.session.query(func.sum(Restock.total_cost)).scalar() or 0
    net_profit = total_revenue - total_purchases
    total_units_sold = db.session.query(db.func.sum(Sale.quantity_sold)).scalar()
    
    top_selling_products = db.session.query(
        Inventory.id,
        Inventory.name,
        func.sum(Sale.quantity_sold).label('units_sold'),
        func.sum(Sale.total_revenue).label('revenue_generated'),
        (func.sum(Sale.total_revenue) - func.coalesce(
            db.session.query(func.sum(Restock.total_cost)).filter(Restock.inventory_id == Inventory.id).as_scalar(), 0)
        ).label('profit_margin')
    ).join(Sale, Inventory.id == Sale.inventory_id)\
     .group_by(Inventory.id, Inventory.name)\
     .order_by(func.sum(Sale.quantity_sold).desc())\
     .limit(10).all()
    
    low_stock_products = db.session.query(
        Inventory.name,
        Inventory.stock_level.label('current_stock'),
        Inventory.min_threshold.label('stock_threshold')
    ).filter(Inventory.stock_level <= Inventory.min_threshold).order_by(Inventory.stock_level.asc()).limit(10).all()
    
    return render_template(
        'statistics.html',
        total_products=total_products,
        healthy_stock=healthy_stock,
        near_min_stock=near_min_stock,
        low_stock=low_stock,
        out_of_stock=out_of_stock,
        total_revenue=total_revenue,
        total_purchases=total_purchases,
        net_profit=net_profit,
        total_units_sold=total_units_sold,
        top_selling_products=top_selling_products,
        low_stock_products=low_stock_products
    )

@statistics_bp.route('/statistics/trends')
@login_required
def sales_purchase_trends():
    daily_sales = db.session.query(
        func.date(Sale.sold_at), func.sum(Sale.total_revenue)
    ).group_by(func.date(Sale.sold_at)).order_by(func.date(Sale.sold_at)).all()
    
    daily_purchases = db.session.query(
        func.date(Restock.restocked_at), func.sum(Restock.total_cost)
    ).group_by(func.date(Restock.restocked_at)).order_by(func.date(Restock.restocked_at)).all()
    
    sales_data = [{'date': str(date), 'revenue': float(revenue)} for date, revenue in daily_sales]
    purchase_data = [{'date': str(date), 'cost': float(cost)} for date, cost in daily_purchases]
    
    return jsonify({'sales': sales_data, 'purchases': purchase_data})
from flask import render_template
from flask_login import login_required
from extensions import db
from models.inventory import Inventory
from models.forecast import Forecast
from models.sales import Sale
from models.history import History
from models.user import User
from models.role import Role
from sqlalchemy.sql import func
from sqlalchemy.sql.functions import coalesce
from datetime import timedelta
from . import reports_bp

@reports_bp.route('/reports')
@login_required
def view():
    # Fetch all inventory items
    inventory_items = Inventory.query.all()

    # Fetch Restock Suggestions (for items below min threshold)
    restock_suggestions = [
        {
            "id": row[0],
            "name": row[1],
            "current_stock": row[2],
            "min_threshold": row[3],
            "forecasted_demand": row[4] or 0,  # Handle None values
            "suggested_amount": max(row[3] - row[2], 0),  # Ensure suggested amount is non-negative
            "priority_level": "High" if row[2] < row[3] * 0.5 else "Medium",
            "time_period": "30 days"
        }
        for row in db.session.query(
            Inventory.id,
            Inventory.name,
            Inventory.stock_level,
            Inventory.min_threshold,
            Forecast.forecasted_demand
        ).outerjoin(Forecast, Forecast.inventory_id == Inventory.id)  # Use outer join in case no forecast exists
        .filter(Inventory.stock_level < Inventory.min_threshold)  # Only show items below min threshold
        .all()
    ]

    # Forecast Accuracy Table (Improved actual demand calculation)
    forecast_accuracy = [
        {
            "inventory_id": row[0],
            "name": row[1],
            "forecasted_demand": row[2],
            "actual_demand": row[3] or 0,  # Handle None values
            "date": row[4]
        }
        for row in db.session.query(
            Forecast.inventory_id,
            Inventory.name,
            Forecast.forecasted_demand,
            coalesce(func.sum(Sale.quantity_sold), 0),  # Use coalesce to handle NULL sums
            Forecast.forecast_date
        )
        .join(Inventory, Inventory.id == Forecast.inventory_id)
        .outerjoin(
            Sale,
            (Sale.inventory_id == Forecast.inventory_id) & 
            (Sale.sold_at.between(Forecast.forecast_date - timedelta(days=7), Forecast.forecast_date + timedelta(days=7)))
        )
        .group_by(
            Forecast.inventory_id,  # Group by inventory_id
            Inventory.name,         # Group by inventory name
            Forecast.forecasted_demand,
            Forecast.forecast_date
        )
        .all()
    ]

    # Updated query for actual demand calculation
    for row in forecast_accuracy:
        actual_sales_query = db.session.query(
            func.sum(Sale.quantity_sold)
        ).filter(
            Sale.inventory_id == row["inventory_id"],
            Sale.sold_at >= (row["date"] - timedelta(days=7)),  # Start window
            Sale.sold_at <= (row["date"] + timedelta(days=7))   # End window
        )
        actual_demand = actual_sales_query.scalar() or 0  # Handle no sales by defaulting to 0
        row["actual_demand"] = actual_demand

    # Fetch top 5 best-selling products
    top_products = db.session.query(
        Sale.inventory_id,
        Inventory.name,
        func.sum(Sale.quantity_sold).label("total_sold")
    ).join(Inventory, Inventory.id == Sale.inventory_id)\
     .group_by(Sale.inventory_id, Inventory.name)\
     .order_by(db.desc("total_sold"))\
     .limit(5)\
     .all()

    # Stock Trends for top-selling products
    stock_trends = {}
    for product in top_products:
        product_trend = db.session.query(
            Sale.sold_at,
            func.sum(Sale.quantity_sold)
        ).filter(Sale.inventory_id == product.inventory_id)\
         .group_by(Sale.sold_at)\
         .order_by(Sale.sold_at)\
         .all()

        stock_trends[product.name] = {
            "dates": [str(row[0]) for row in product_trend],
            "levels": [row[1] for row in product_trend]
        }

    # Fetch history records with user and role information
    history_records = db.session.query(
        History.id,
        History.description,
        History.timestamp,
        User.username,
        Role.name.label('role_name')
    ).join(User, User.id == History.user_id)\
     .join(Role, Role.id == User.role_id)\
     .order_by(History.id.desc())\
     .all()

    # Format history records for template
    formatted_history_records = [
        {
            "user_role": record.role_name,
            "username": record.username,
            "description": record.description,
            "timestamp": record.timestamp
        }
        for record in history_records
    ]

    return render_template(
        'reports.html',
        inventory_items=inventory_items,
        forecast_accuracy=forecast_accuracy,
        restock_suggestions=restock_suggestions,
        stock_trends=stock_trends,
        history_records=formatted_history_records  # Pass formatted history records
    )
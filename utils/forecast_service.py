from models.inventory import Inventory
from models.forecast import Forecast
from models.sales import Sale
from models.restock import Restock
from extensions import db
import numpy as np
from sklearn.linear_model import LinearRegression

def generate_stock_forecast(inventory_id=None):
    """
    Generate forecasted stock demand using linear regression.
    If inventory_id is provided, forecast for that item. Otherwise, forecast for all items.
    """
    inventory_items = Inventory.query.all() if inventory_id is None else [Inventory.query.get(inventory_id)]

    for item in inventory_items:
        if not item:
            continue  # Skip if the item does not exist

        # Fetch historical sales data (use the Sale table instead of History)
        sales_data = Sale.query.filter_by(inventory_id=item.id).order_by(Sale.sold_at).all()
        
        if len(sales_data) < 2:
            continue  # Not enough data for a reliable forecast

        # Prepare data for regression
        X = np.array(range(len(sales_data))).reshape(-1, 1)  # Time points
        y = np.array([entry.quantity_sold for entry in sales_data])  # Quantities sold over time

        model = LinearRegression()
        model.fit(X, y)
        forecasted_value = max(0, int(model.predict([[len(sales_data) + 1]])[0]))  # Avoid negative forecasts

        # Update or insert forecasted data
        forecast_entry = Forecast.query.filter_by(inventory_id=item.id).first()
        if forecast_entry:
            forecast_entry.forecasted_demand = forecasted_value
        else:
            forecast_entry = Forecast(inventory_id=item.id, forecasted_demand=forecasted_value)
            db.session.add(forecast_entry)

    db.session.commit()

import os
from flask import render_template, request, redirect, url_for, flash, jsonify, current_app, Blueprint
from flask_login import login_required, current_user
from extensions import db
from models.inventory import Inventory
from models.category import Category
from models.unit_type import UnitType
from models.restock import Restock
from models.notification import Notification
from datetime import datetime

inventory_bp = Blueprint('inventory', __name__)

@inventory_bp.route('/inventory')
@login_required
def view():
    inventory_items = Inventory.query.all()
    categories = Category.query.all()
    unit_types = UnitType.query.all()
    return render_template('inventory.html', inventory=inventory_items, categories=categories, unit_types=unit_types)

@inventory_bp.route('/inventory/add', methods=['POST'])
@login_required
def add_item():
    name = request.form['name']
    category_id = request.form['category_id']
    unit_type_id = request.form['unit_type_id']
    cost_price = float(request.form['cost_price'])
    selling_price = float(request.form['selling_price'])
    item_code = request.form['item_code']
    stock_level = int(request.form['stock_level'])
    min_threshold = int(request.form['min_threshold'])
    max_threshold = int(request.form['max_threshold'])

    # Validate initial stock level
    if stock_level > max_threshold:
        flash("Initial stock level cannot exceed the maximum threshold.", "danger")
        return redirect(url_for('inventory.view'))

    # Check for duplicate item code
    if Inventory.query.filter_by(item_code=item_code).first():
        flash("Item code already exists. Please use a different code.", "danger")
        return redirect(url_for('inventory.view'))

    # Create new inventory item
    new_item = Inventory(
        name=name, category_id=category_id, unit_type_id=unit_type_id,
        cost_price=cost_price, selling_price=selling_price, item_code=item_code,
        stock_level=stock_level, min_threshold=min_threshold, max_threshold=max_threshold,
        image=None, created_by=current_user.id
    )
    db.session.add(new_item)
    db.session.flush()  # Ensures new_item.id is available

    image_filename = None
    if 'image' in request.files:
        image = request.files['image']
        if image.filename:
            ext = image.filename.rsplit('.', 1)[1].lower()
            image_filename = f"inventory_{new_item.id}.{ext}"
            image.save(os.path.join(current_app.config['INVENTORY_UPLOAD_FOLDER'], image_filename))
            new_item.image = image_filename

    # Add initial stock to the restock table
    if stock_level > 0:
        initial_restock = Restock(
            inventory_id=new_item.id,
            quantity_added=stock_level,
            cost_price_at_time=cost_price,
            total_cost=stock_level * cost_price  # Calculate total cost
        )
        db.session.add(initial_restock)

    db.session.commit()

    # Log notification
    notification = Notification(
        user_id=current_user.id,
        action_type="add",
        entity_type="inventory",
        description=f"added inventory item: {name}",
        timestamp=datetime.utcnow()
    )
    db.session.add(notification)
    db.session.commit()

    flash("Inventory item added successfully!", "success")
    return redirect(url_for('inventory.view'))

@inventory_bp.route('/inventory/edit/<int:item_id>', methods=['POST'])
@login_required
def edit_item(item_id):
    item = Inventory.query.get(item_id)
    old_name = item.name

    item.name = request.form['name']
    item.category_id = request.form['category_id']
    item.unit_type_id = request.form['unit_type_id']
    item.cost_price = float(request.form['cost_price'])
    item.selling_price = float(request.form['selling_price'])
    item.item_code = request.form['item_code']
    item.min_threshold = int(request.form['min_threshold'])
    item.max_threshold = int(request.form['max_threshold'])

    # Validate max threshold
    if item.max_threshold < item.stock_level:
        flash("Maximum threshold cannot be lower than the current stock level.", "danger")
        return redirect(url_for('inventory.view'))

    if 'image' in request.files:
        image = request.files['image']
        if image.filename:
            ext = image.filename.rsplit('.', 1)[1].lower()
            image_filename = f"inventory_{item.id}.{ext}"
            image.save(os.path.join(current_app.config['INVENTORY_UPLOAD_FOLDER'], image_filename))
            item.image = image_filename

    db.session.commit()

    # Log notification
    if old_name == item.name:
        description = f"edited inventory item: {old_name}"
    else:
        description = f"edited inventory item: {old_name} to {item.name}"

    notification = Notification(
        user_id=current_user.id,
        action_type="edit",
        entity_type="inventory",
        description=description,
        timestamp=datetime.utcnow()
    )
    db.session.add(notification)
    db.session.commit()

    flash("Inventory item updated successfully!", "success")
    return redirect(url_for('inventory.view'))

@inventory_bp.route('/inventory/delete/<int:item_id>', methods=['POST'])
@login_required
def delete_item(item_id):
    item = Inventory.query.get(item_id)
    
    if not item:
        flash("Inventory item not found.", "danger")
        return redirect(url_for('inventory.view'))
    
    name = item.name
    db.session.delete(item)
    db.session.commit()

    # Log notification
    notification = Notification(
        user_id=current_user.id,
        action_type="delete",
        entity_type="inventory",
        description=f"deleted inventory item: {name}",
        timestamp=datetime.utcnow()
    )
    db.session.add(notification)
    db.session.commit()

    flash("Inventory item deleted successfully!", "danger")
    return redirect(url_for('inventory.view'))

@inventory_bp.route('/inventory/check_item_code', methods=['POST'])
@login_required
def check_item_code():
    item_code = request.json.get('item_code')
    exists = Inventory.query.filter_by(item_code=item_code).first() is not None
    return jsonify({'exists': exists})
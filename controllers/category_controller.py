from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models.category import Category
from models.notification import Notification
from datetime import datetime
from . import category_bp

@category_bp.route('/categories')
@login_required
def view():
    categories = Category.query.all()
    return render_template('category.html', categories=categories)

@category_bp.route('/categories/add', methods=['POST'])
@login_required
def add_category():
    name = request.form['name']
    description = request.form['description']

    new_category = Category(name=name, description=description)
    db.session.add(new_category)
    db.session.commit()

    # Log notification
    notification = Notification(
        user_id=current_user.id,
        action_type="add",
        entity_type="category",
        description=f"added category: {name}",
        timestamp=datetime.utcnow()
    )
    db.session.add(notification)
    db.session.commit()

    flash("Category added successfully!", "success")
    return redirect(url_for('category.view'))  

@category_bp.route('/categories/edit/<int:category_id>', methods=['POST'])
@login_required
def edit_category(category_id):
    category = Category.query.get(category_id)
    old_name = category.name

    category.name = request.form['name']
    category.description = request.form['description']

    db.session.commit()

    # Log notification
    if old_name == category.name:
        description = f"edited category: {old_name}"
    else:
        description = f"edited category: {old_name} to {category.name}"

    notification = Notification(
        user_id=current_user.id,
        action_type="edit",
        entity_type="category",
        description=description,
        timestamp=datetime.utcnow()
    )
    db.session.add(notification)
    db.session.commit()

    flash("Category updated successfully!", "success")
    return redirect(url_for('category.view'))  

@category_bp.route('/categories/delete/<int:category_id>', methods=['POST'])
@login_required
def delete_category(category_id):
    category = Category.query.get(category_id)
    name = category.name
    db.session.delete(category)
    db.session.commit()

    # Log notification
    notification = Notification(
        user_id=current_user.id,
        action_type="delete",
        entity_type="category",
        description=f"deleted category: {name}",
        timestamp=datetime.utcnow()
    )
    db.session.add(notification)
    db.session.commit()

    flash("Category deleted successfully!", "danger")
    return redirect(url_for('category.view'))

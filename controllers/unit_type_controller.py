from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask_login import login_required, current_user
from extensions import db
from models.unit_type import UnitType
from models.notification import Notification
from datetime import datetime
from . import unit_type_bp

@unit_type_bp.route('/unit_types')
@login_required
def view():
    unit_types = UnitType.query.all()
    return render_template('unit_type.html', unit_types=unit_types)

@unit_type_bp.route('/unit_types/add', methods=['POST'])
@login_required
def add_unit_type():
    name = request.form['name']
    description = request.form['description']

    new_unit_type = UnitType(name=name, description=description)
    db.session.add(new_unit_type)
    db.session.commit()

    # Log notification
    notification = Notification(
        user_id=current_user.id,
        action_type="add",
        entity_type="unit_type",
        description=f"added unit type: {name}",
        timestamp=datetime.utcnow()
    )
    db.session.add(notification)
    db.session.commit()

    flash("Unit type added successfully!", "success")
    return redirect(url_for('unit_type.view'))  

@unit_type_bp.route('/unit_types/edit/<int:unit_type_id>', methods=['POST'])
@login_required
def edit_unit_type(unit_type_id):
    unit_type = UnitType.query.get(unit_type_id)
    old_name = unit_type.name

    unit_type.name = request.form['name']
    unit_type.description = request.form['description']

    db.session.commit()

    # Log notification
    if old_name == unit_type.name:
        description = f"edited unit type: {old_name}"
    else:
        description = f"edited unit type: {old_name} to {unit_type.name}"

    notification = Notification(
        user_id=current_user.id,
        action_type="edit",
        entity_type="unit_type",
        description=description,
        timestamp=datetime.utcnow()
    )
    db.session.add(notification)
    db.session.commit()

    flash("Unit type updated successfully!", "success")
    return redirect(url_for('unit_type.view'))  

@unit_type_bp.route('/unit_types/delete/<int:unit_type_id>', methods=['POST'])
@login_required
def delete_unit_type(unit_type_id):
    unit_type = UnitType.query.get(unit_type_id)
    name = unit_type.name
    db.session.delete(unit_type)
    db.session.commit()

    # Log notification
    notification = Notification(
        user_id=current_user.id,
        action_type="delete",
        entity_type="unit_type",
        description=f"deleted unit type: {name}",
        timestamp=datetime.utcnow()
    )
    db.session.add(notification)
    db.session.commit()

    flash("Unit type deleted successfully!", "danger")
    return redirect(url_for('unit_type.view'))

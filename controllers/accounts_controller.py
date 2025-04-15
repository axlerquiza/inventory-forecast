from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from extensions import db, bcrypt
from models.user import User
from models.notification import Notification
from . import accounts_bp
from flask_login import current_user
from datetime import datetime

@accounts_bp.route('/accounts')
@login_required
def view():
    users = User.query.all()
    return render_template('accounts.html', users=users)

@accounts_bp.route('/accounts/add', methods=['POST'])
@login_required
def add_user():
    username = request.form['username']
    email = request.form['email']  # Get email from form
    password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
    role_id = int(request.form['role'])

    # Check for duplicate username or email
    if User.query.filter_by(username=username).first():
        flash("Username already exists. Please use a different username.", "danger")
        return redirect(url_for('accounts.view'))
    if User.query.filter_by(email=email).first():
        flash("Email already exists. Please use a different email.", "danger")
        return redirect(url_for('accounts.view'))

    new_user = User(username=username, email=email, password=password, role_id=role_id)
    db.session.add(new_user)
    db.session.commit()

    # Log notification
    notification = Notification(
        user_id=current_user.id,
        action_type="add",
        entity_type="account",
        description=f"added account: {username}",
        timestamp=datetime.utcnow()
    )
    db.session.add(notification)
    db.session.commit()

    flash("Account added successfully!", "success")
    return redirect(url_for('accounts.view'))

@accounts_bp.route('/accounts/edit/<int:user_id>', methods=['POST'])
@login_required
def edit_user(user_id):
    user = User.query.get(user_id)
    old_username = user.username
    user.username = request.form['username']
    user.email = request.form['email']
    user.role_id = int(request.form['role'])

    # Check for duplicate email (excluding the current user)
    if User.query.filter(User.email == user.email, User.id != user.id).first():
        flash("Email already exists. Please use a different email.", "danger")
        return redirect(url_for('accounts.view'))

    db.session.commit()

    # Log notification
    if old_username == user.username:
        description = f"edited account: {old_username}"
    else:
        description = f"edited account: {old_username} to {user.username}"

    notification = Notification(
        user_id=current_user.id,
        action_type="edit",
        entity_type="account",
        description=description,
        timestamp=datetime.utcnow()
    )
    db.session.add(notification)
    db.session.commit()

    flash("User updated successfully!", "success")
    return redirect(url_for('accounts.view'))

@accounts_bp.route('/accounts/delete/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    user = User.query.get(user_id)
    username = user.username
    db.session.delete(user)
    db.session.commit()

    # Log notification
    notification = Notification(
        user_id=current_user.id,
        action_type="delete",
        entity_type="account",
        description=f"deleted account: {username}",
        timestamp=datetime.utcnow()
    )
    db.session.add(notification)
    db.session.commit()

    flash("User deleted successfully!", "danger")
    return redirect(url_for('accounts.view'))
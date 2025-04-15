import os
from flask import render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from extensions import db, bcrypt  # Import bcrypt for password hashing and checking
from models.user import User
from . import profile_bp

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

@profile_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def view():
    if request.method == 'POST':
        # Update first name: Save as None if the input is empty
        first_name = request.form.get('first_name', "").strip()
        current_user.first_name = first_name if first_name else None

        # Update last name: Save as None if the input is empty
        last_name = request.form.get('last_name', "").strip()
        current_user.last_name = last_name if last_name else None

        # Update email: Ensure it is not null
        email = request.form.get('email', "").strip()
        if not email:  # Check if the email is empty
            flash("Email cannot be empty. Please provide a valid email address.", "danger")
            return redirect(url_for('profile.view'))

        if email != current_user.email:  # Only update if the email is different
            existing_user = User.query.filter_by(email=email).first()
            if existing_user and existing_user.id != current_user.id:
                flash("Email already exists. Please use a different one.", "danger")
                return redirect(url_for('profile.view'))
            current_user.email = email

        # Update phone number: Save as None if the input is empty
        phone_number = request.form.get('phone_number', "").strip()
        current_user.phone_number = phone_number if phone_number else None

        # Handle profile picture upload
        if 'profile_picture' in request.files:
            file = request.files['profile_picture']
            if file and allowed_file(file.filename):
                ext = file.filename.rsplit('.', 1)[1].lower()
                filename = f"user_{current_user.id}.{ext}"
                filepath = os.path.join(current_app.config['PROFILE_PIC_FOLDER'], filename)

                # Delete old picture if exists & not default
                if current_user.profile_picture and "default" not in current_user.profile_picture:
                    old_picture_path = os.path.join(current_app.config['PROFILE_PIC_FOLDER'], current_user.profile_picture)
                    if os.path.exists(old_picture_path):
                        os.remove(old_picture_path)

                file.save(filepath)
                current_user.profile_picture = filename  # Update filename in DB

        # Commit changes to the database
        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for('profile.view'))

    return render_template('profile.html')

@profile_bp.route('/profile/change_password', methods=['POST'])
@login_required
def change_password():
    current_password = request.form.get('current_password', '').strip()
    new_password = request.form.get('new_password', '').strip()
    confirm_new_password = request.form.get('confirm_new_password', '').strip()

    # Ensure all fields are filled
    if not current_password or not new_password or not confirm_new_password:
        flash("All password fields are required.", "danger")
        return redirect(url_for('profile.view'))

    # Validate current password
    if not bcrypt.check_password_hash(current_user.password, current_password):
        flash("Current password is incorrect.", "danger")
        return redirect(url_for('profile.view'))

    # Check if new password matches confirmation
    if new_password != confirm_new_password:
        flash("New passwords do not match.", "danger")
        return redirect(url_for('profile.view'))

    # Check if new password is same as current
    if bcrypt.check_password_hash(current_user.password, new_password):
        flash("New password must be different from the current password.", "danger")
        return redirect(url_for('profile.view'))

    # Hash and save new password
    hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
    current_user.password = hashed_password
    db.session.commit()

    flash("Password changed successfully!", "success")
    return redirect(url_for('profile.view'))
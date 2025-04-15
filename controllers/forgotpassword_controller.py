from flask import render_template, request, redirect, url_for, flash
from extensions import db, bcrypt
from models.user import User
from . import forgotpassword_bp
import random
import string

@forgotpassword_bp.route('/forgot_password', methods=['GET', 'POST'])
def view():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()

        if not user:
            flash("Email not found. Please try again.", "danger")
            return redirect(url_for('forgotpassword.view'))

        # Generate a random 8-character password
        new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')

        # Update the user's password
        user.password = hashed_password
        db.session.add(user)  # Ensure the user object is added to the session
        db.session.commit()

        # Redirect to a page that displays the new password
        return redirect(url_for('forgotpassword.display_new_password', new_password=new_password))

    return render_template('forgot_password.html')

@forgotpassword_bp.route('/display_new_password')
def display_new_password():
    new_password = request.args.get('new_password')
    if not new_password:
        flash("No password to display. Please try again.", "danger")
        return redirect(url_for('forgotpassword.view'))

    return render_template('display_new_password.html', new_password=new_password)
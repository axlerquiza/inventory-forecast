from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required
from extensions import bcrypt
from models.user import User
from . import auth_bp
from urllib.parse import urlparse, urljoin

# Utility function to check if a URL is safe for redirection
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get the user from the database using the username
        user = User.query.filter_by(username=request.form['username']).first()
        
        if user and bcrypt.check_password_hash(user.password, request.form['password']):
            # Log the user in if the password matches
            login_user(user)

            # Get the "next" URL from the request arguments (if any)
            next_page = request.args.get('next')
            if next_page and is_safe_url(next_page):
                return redirect(next_page)  # Redirect to the "next" page
            else:
                return redirect(url_for('dashboard.view'))  # Default redirect

        # If username or password is incorrect, show a flash message
        flash('Invalid username or password', 'danger')

    # Render the login template
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    # Log out the current user
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))  
